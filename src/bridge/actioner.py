#!/usr/bin/python
#####################################################################
# Cloud Routes: Actioner (aka Sink)
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This process will recieve messages from the workers
# the messages will tell the sink wether the health check is a
# successful or unsuccessful.
# ------------------------------------------------------------------
# Original Author: Benjamin J. Cane - @madflojo
# Contributors:
# - Benjamin Cane - @madflojo
#####################################################################


# Imports
# ------------------------------------------------------------------

# Import Modules
import sys
import yaml
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import socket
import redis
import signal
import logconfig
import zmq
import json
import time

# Load Configuration
# ------------------------------------------------------------------

if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]
cfh = open(configfile, "r")
config = yaml.safe_load(cfh)
cfh.close()


# Open External Connections
# ------------------------------------------------------------------

# Init logger
logger = logconfig.getLogger('bridge.actioner', config['use_syslog'])

logger.info("Using config %s" % configfile)

# Redis Server
try:
    r_server = redis.Redis(
        host=config['redis_host'], port=config['redis_port'],
        db=config['redis_db'], password=config['redis_password'])
    logger.info("Connected to Redis on port %s" % config['redis_port'])
except:
    logger.error("Cannot connect to redis, shutting down")
    sys.exit(1)

# RethinkDB Server
try:
    rdb_server = r.connect(
        host=config['rethink_host'], port=config['rethink_port'],
        auth_key=config['rethink_authkey'], db=config['rethink_db'])
    logger.info("Connected to Rethinkdb on port %s" % config['rethink_port'])
    cacheonly = False
except (RqlDriverError, RqlRuntimeError, socket.error) as e:
    logger.critical("Cannot connect to rethinkdb, going into cacheonly mode")
    logger.critical("RethinkDB: %s" % e.message)
    cacheonly = True
    rdb_server = None


# Start ZeroMQ listener
context = zmq.Context()
zsink = context.socket(zmq.PULL)
connectline = "tcp://%s:%d" % (config['sink_ip'], config['sink_worker_port'])
logger.info("Connecting to Broker at %s" % connectline)
zsink.connect(connectline)
logger.info("Connection to Broker established")


# Handle Kill Signals Cleanly
# ------------------------------------------------------------------

def killhandle(signum, frame):
    ''' This will close connections cleanly '''
    logger.info("SIGTERM detected, shutting down")
    rdb_server.close()
    zsink.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)

# Local functions
# ------------------------------------------------------------------


def runAction(**kwargs):
    ''' Run reactions in a function '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    reaction = __import__(
        "actions." + redata['rtype'], globals(), locals(), ['action'], -1)
    try:
        react = reaction.action(redata=kwargs['redata'], jdata=kwargs['jdata'],
            rdb=kwargs['rdb'], r_server=kwargs['r_server'], config=kwargs['config'])
    except Exception as e:
        logger.error("Got error when attempting to run reaction %s for monitor %s" % (
            redata['rtype'], jdata['cid']))
        logger.error(e)
        react = False
    if react is True:
        logger.info("Successfully processed %s reaction type %s for monitor %s" % (
            jdata['check']['status'], redata['rtype'], jdata['cid']))
        return True
    elif react is None:
        logger.info("Skipped %s reaction type %s for monitor %s" % (
            jdata['check']['status'], redata['rtype'], jdata['cid']))
        return None
    else:
        logger.info("Processing %s reaction type %s for monitor %s did not occur" % (
            jdata['check']['status'], redata['rtype'], jdata['cid']))
        return False


def lookupRedis(itemkey, itemid):
    ''' Lookup a redis hash '''
    results = {'id': itemid}
    cachekey = itemkey + ":" + itemid
    for key in r_server.hkeys(cachekey):
        value = r_server.hget(cachekey, key)
        if value == "slist":
            results[key] = []
            listkey = cachekey + ":" + key
            for entry in r_server.smembers(listkey):
                results[key].append(entry)
        else:
            results[key] = value
    cachekey = itemkey + ":" + itemid + ":data"
    for key in r_server.hkeys(cachekey):
        value = r_server.hget(cachekey, key)
        if value == "slist":
            results[key] = []
            listkey = cachekey + ":" + key
            for entry in r_server.smembers(listkey):
                results[key].append(entry)
        else:
            results[key] = value
    return results


def getMonitor(cid):
    ''' Lookup a monitor via either rethinkdb or redis '''
    # Pull from redis first
    cache = lookupRedis("monitor", cid)

    # Pull from RethinkDB second
    try:
        results = r.table('monitors').get(cid).run(rdb_server)
        results['cacheonly'] = False
        if int(cache['failcount']) > results['failcount']:
            results['failcount'] = int(cache['failcount'])
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        results = cache
        results['cacheonly'] = True
        logger.critical("RethinkDB is unaccessible, monitor %s was pulled from cache" % cid)
        logger.critical("RethinkDB Error: %s" % e.message)
    return results


def getReaction(rid):
    ''' Lookup a reaction via either rethinkdb or redis '''
    # Pull from redis first
    cache = lookupRedis("reaction", rid)
    # Resolve issues form race condition during editing of reactions
    if "lastrun" in cache:
        if cache['lastrun'] is None or cache['lastrun'] is "None":
            # Reset lastrun to 0 if it is not present or set to None
            cache['lastrun'] = 0
    else:
        cache['lastrun'] = 0

    # Pull from RethinkDB second
    try:
        results = r.table('reactions').get(rid).run(rdb_server)
        if results['lastrun'] is None:
            results['lastrun'] = 0
        results['cacheonly'] = False
        if int(cache['trigger']) > results['trigger']:
            results['trigger'] = int(cache['trigger'])
        if float(cache['lastrun']) > float(results['lastrun']):
            results['lastrun'] = float(cache['lastrun'])
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        results = cache
        results['cacheonly'] = True
        logger.critical("RethinkDB is unaccessible, reaction %s was pulled from cache" % rid)
        logger.critical("RethinkDB Error: %s" % e.message)
    return results

# Run For Loop
# ------------------------------------------------------------------

while True:
    msg = zsink.recv()
    logger.debug("Got message %s" % msg)

    jdata = json.loads(msg)
    logger.info("Got message for health check: %s" % jdata['cid'])

    checktime = time.time() - jdata['time_tracking']['control']
    if checktime > float(config['max_monitor_time']):
        logger.critical("CRITICAL ERROR: monitor %s is beyond %d second execution time. SKIPPING" % (jdata['cid'], config['max_monitor_time']))
    else:
        results = getMonitor(jdata['cid'])
        jdata['cacheonly'] = results['cacheonly']
        jdata['check']['prev_status'] = results['status']

        # Check if status is changing and reset counter
        if jdata['check']['prev_status'] in jdata['check']['status']:
            jdata['failcount'] = results['failcount']
        else:
            jdata['prev_failcount'] = results['failcount']
            jdata['failcount'] = 0

        # Ensure reactions run on manual failures
        if jdata['check']['method'] == "manual" and jdata['check']['status'] == "web-false":
            jdata['failcount'] = 9999

        if results['status'] != "web-false" or jdata['check']['method'] == "manual":

            # Start running through normal reactions
            for reactid in jdata['data']['reactions']:
                results = getReaction(reactid)
                if results:
                    results['default'] = False
                    run = runAction(redata=results, jdata=jdata,
                        rdb=rdb_server, r_server=r_server, config=config)
                    for meta in config['reaction_meta']:
                        results['rtype'] = meta
                        results['lastrun'] = 0
                        results['trigger'] = 0
                        results['frequency'] = 0
                        results['reaction_return'] = run
                        runAction(redata=results, jdata=jdata,
                            rdb=rdb_server, r_server=r_server, config=config)

            # Always perform the default actions
            for always in config['default_actions']:
                redata = {'rtype': always,
                          'trigger': 0,
                          'frequency': 0,
                          'lastrun': 0,
                          'default': True}
                runAction(redata=redata, jdata=jdata,
                    rdb=rdb_server, r_server=r_server, config=config)

        if cacheonly is True:
            logger.critical("Process is in cacheonly mode: attempting reconnect")
            try:
                rdb_server.reconnect()
                logger.info("Connected to Rethinkdb on port %s" % config['rethink_port'])
                cacheonly = False
            except (RqlDriverError, RqlRuntimeError) as e:
                logger.critical("RethinkDB Error: %s" % e.message)
            except:
                logger.critical("Got non-RethinkDB Error... I should be restarted when RethinkDB is up")
