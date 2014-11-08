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
import syslog
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

# Open Syslog
syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL0)

# Redis Server
try:
    r_server = redis.Redis(
        host=config['redis_host'], port=config['redis_port'],
        db=config['redis_db'], password=config['redis_password'])
    line = "Connected to Redis on port %s" % config['redis_port']
    syslog.syslog(syslog.LOG_INFO, line)
except:
    line = "Cannot connect to redis, shutting down"
    syslog.syslog(syslog.LOG_ERR, line)
    sys.exit(1)

# RethinkDB Server
try:
    rdb_server = r.connect(
        host=config['rethink_host'], port=config['rethink_port'],
        auth_key=config['rethink_authkey'], db=config['rethink_db'])
    line = "Connected to Rethinkdb on port %s" % config['rethink_port']
    syslog.syslog(syslog.LOG_INFO, line)
    cacheonly = False
except (RqlDriverError, RqlRuntimeError, socket.error) as e:
    line = "Cannot connect to rethinkdb, going into cacheonly mode"
    syslog.syslog(syslog.LOG_CRIT, line)
    line = "RethinkDB: %s" % e.message
    syslog.syslog(syslog.LOG_CRIT, line)
    cacheonly = True
    rdb_server = None


# Start ZeroMQ listener
context = zmq.Context()
zsink = context.socket(zmq.PULL)
connectline = "tcp://%s:%d" % (config['sink_ip'], config['sink_worker_port'])
line = "Connecting to Broker at %s" % connectline
syslog.syslog(syslog.LOG_INFO, line)
zsink.connect(connectline)
line = "Connection to Broker established"
syslog.syslog(syslog.LOG_INFO, line)


# Handle Kill Signals Cleanly
# ------------------------------------------------------------------

def killhandle(signum, frame):
    ''' This will close connections cleanly '''
    line = "SIGTERM detected, shutting down"
    syslog.syslog(syslog.LOG_INFO, line)
    rdb_server.close()
    syslog.closelog()
    zsink.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)

# Local functions
# ------------------------------------------------------------------


def runAction(redata, jdata):
    ''' Run reactions in a function '''
    if "failed" in jdata['check']['status']:
        reaction = __import__(
            "actions." + redata['rtype'], globals(), locals(), ['failed'], -1)
        react = reaction.failed(redata, jdata, rdb_server, r_server)
        if react is True:
            line = "Successfully processed failed reaction type %s for monitor %s" % (
                redata['rtype'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return True
        elif react is None:
            line = "Skipped failed reaction type %s for monitor %s" % (
                redata['rtype'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return None
        else:
            line = "Processing reaction type %s for monitor %s did not occur" % (
                redata['rtype'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return False
    elif "healthy" in jdata['check']['status']:
        reaction = __import__(
            "actions." + redata['rtype'], globals(), locals(), ['healthy'], -1)
        react = reaction.healthy(redata, jdata, rdb_server, r_server)
        if react:
            line = "Successfully processed healthy reaction type %s for monitor %s" % (
                redata['rtype'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return True
        elif react is None:
            line = "Skipped healthy reaction type %s for monitor %s" % (
                redata['rtype'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return None
        else:
            line = "Error while processing healthy reaction type %s for monitor %s" % (
                redata['rtype'], jdata['cid'])
            syslog.syslog(syslog.LOG_INFO, line)
            return False
    else:
        line = "Got an unknown status for health check %s: %s" % (
            jdata['cid'], jdata['status'])
        syslog.syslog(syslog.LOG_ERR, line)
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
        line = "RethinkDB is unaccessible, monitor %s was pulled from cache" % cid
        syslog.syslog(syslog.LOG_CRIT, line)
        line = "RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_CRIT, line)
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
        line = "RethinkDB is unaccessible, reaction %s was pulled from cache" % rid
        syslog.syslog(syslog.LOG_CRIT, line)
        line = "RethinkDB Error: %s" % e.message
        syslog.syslog(syslog.LOG_CRIT, line)
    return results

# Run For Loop
# ------------------------------------------------------------------

while True:
    msg = zsink.recv()
    line = "Got message %s" % msg
    syslog.syslog(syslog.LOG_DEBUG, line)

    jdata = json.loads(msg)
    line = "Got message for health check: %s" % jdata['cid']
    syslog.syslog(syslog.LOG_INFO, line)

    checktime = time.time() - jdata['time_tracking']['control']
    if checktime > float(config['max_monitor_time']):
      line = "CRITICAL ERROR: monitor %s is beyond %d second execution time" % (jdata['cid'], config['max_monitor_time'])
      syslog.syslog(syslog.LOG_CRIT, line)

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
    if jdata['check']['method'] == "manual" and jdata['check']['status'] == "web-failed":
        jdata['failcount'] = 9999

    if results['status'] != "web-failed" or jdata['check']['method'] == "manual":

        # Start running through normal reactions
        for reactid in jdata['data']['reactions']:
            results = getReaction(reactid)
            if results:
                results['default'] = False
                run = runAction(results, jdata)
                for meta in config['reaction_meta']:
                    results['rtype'] = meta
                    results['lastrun'] = 0
                    results['trigger'] = 0
                    results['frequency'] = 0
                    results['reaction_return'] = run
                    runAction(results, jdata)

        # Always perform the default actions
        for always in config['default_actions']:
            redata = {'rtype': always,
                      'trigger': 0,
                      'frequency': 0,
                      'lastrun': 0,
                      'default': True}
            runAction(redata, jdata)

    if cacheonly is True:
        line = "Process is in cacheonly mode: attempting reconnect"
        syslog.syslog(syslog.LOG_CRIT, line)
        try:
            rdb_server.reconnect()
            line = "Connected to Rethinkdb on port %s" % config['rethink_port']
            syslog.syslog(syslog.LOG_INFO, line)
            cacheonly = False
        except (RqlDriverError, RqlRuntimeError) as e:
            line = "RethinkDB Error: %s" % e.message
            syslog.syslog(syslog.LOG_CRIT, line)
        except:
            line = "Got non-RethinkDB Error... I should be restarted when RethinkDB is up"
            syslog.syslog(syslog.LOG_CRIT, line)
