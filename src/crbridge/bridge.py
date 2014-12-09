#!/usr/bin/python
#####################################################################
# Cloud Routes Bridge
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is a bridge application between the web interface of
# cloudrout.es and the backend cloud routes availability maanger.
# This will gather queue tasks from rethinkdb and create/delete
# the appropriate monitor in the action processes.
# ------------------------------------------------------------------
# Original Author: Benjamin J. Cane - @madflojo
# Maintainers:
# - Benjamin Cane - @madflojo
#####################################################################


# Imports
# ------------------------------------------------------------------

# Clean Paths for All
import sys
import yaml
import rethinkdb as r
from rethinkdb.errors import RqlDriverError
import redis
import signal
import logconfig
import time
import zmq
import json


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
logger = logconfig.getLogger('crbridge.bridge', config['use_syslog'])

logger.info("Using config %s" % configfile)

# Redis Server
try:
    r_server = redis.Redis(
        host=config['redis_host'], port=config['redis_port'],
        db=config['redis_db'], password=config['redis_password'])
    logger.info("Connecting to redis")
except:
    logger.error("Cannot connect to redis, shutting down")
    sys.exit(1)

# RethinkDB Server
try:
    rdb_server = r.connect(
        host=config['rethink_host'], port=config['rethink_port'],
        auth_key=config['rethink_authkey'], db=config['rethink_db'])
    logger.info("Connecting to RethinkDB")
except RqlDriverError:
    logger.error("Cannot connect to rethinkdb, shutting down")
    sys.exit(1)

# Sink
context = zmq.Context()
zsend = context.socket(zmq.PUSH)
connectline = "tcp://%s:%d" % (config['sink_ip'], config['sink_port'])
logger.info("Connecting to Sink at %s" % connectline)
zsend.connect(connectline)


# Handle Kill Signals Cleanly
# ------------------------------------------------------------------

def killhandle(signum, frame):
    ''' This will close connections cleanly '''
    logger.info("SIGTERM detected, shutting down")
    rdb_server.close()
    zsend.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)


# Helper Functions
# ------------------------------------------------------------------

def populateRedis(itemkey, item, local=False):
    '''
    This will parse out a dictionary and return lists keys and dict values
    '''
    for entry in item.keys():
        if entry == "data":
            for key in item['data'].keys():
                if key == "timer" and local is True:
                    r_server.sadd(item['data'][key], item['cid'])
                if type(item['data'][key]) is list:
                    r_server.hset(itemkey + ":data", key, "slist")
                    sid = "%s:data:%s" % (itemkey, key)
                    for entry in item['data'][key]:
                        r_server.sadd(sid, entry)
                else:
                    r_server.hset(itemkey + ":data", key, item['data'][key])
        else:
            r_server.hset(itemkey, entry, item[entry])
    return True


def decimateRedis(itemkey, item):
    ''' This will parse out a dictionary and kill the redis data '''
    if "timer" in item['data']:
        r_server.srem(item['data']['timer'], item['cid'])
    keys = r_server.hkeys(itemkey)
    for key in keys:
        value = r_server.hget(itemkey, key)
        if value == "slist":
            skey = itemkey + ":" + key
            for member in r_server.smembers(skey):
                r_server.srem(skey, member)
        r_server.hdel(itemkey, key)
    keys = r_server.hkeys(itemkey + ":data")
    for key in keys:
        value = r_server.hget(itemkey + ":data", key)
        if value == "slist":
            skey = itemkey + ":data:" + key
            for member in r_server.smembers(skey):
                r_server.srem(skey, member)
        r_server.hdel(itemkey + ":data", key)
    return True


def sendtoSink(item):
    ''' This will send a manual action to the sink '''
    msg = item
    msg['time_tracking'] = {
        'control': time.time(),
        'ez_key': config['stathat_key'],
        'env': config['envname']}
    msg['zone'] = "Web API"
    jdata = json.dumps(msg)
    zsend.send(jdata)
    return True


# Run
# ------------------------------------------------------------------

# On Startup Synchronize transaction logs
recount = 0
for item in r_server.smembers("history"):
    record = json.loads(item)
    try:
        results = r.table("history").insert(record).run(rdb_server)
        success = True
    except:
        success = False

    if success:
        r_server.srem("history", item)
        recount = recount + 1
logger.info("Imported %d history records from cache to rethinkDB" % recount)

# On Startup Synchronize event logs
recount = 0
for item in r_server.smembers("events"):
    record = json.loads(item)
    try:
        results = r.table("events").insert(record).run(rdb_server)
        success = True
    except:
        success = False

    if success:
        r_server.srem("events", item)
        recount = recount + 1
logger.info("Imported %d events records from cache to rethinkDB" % recount)

# Run the queue watcher
while True:
    results = r.table(config['dbqueue']).run(rdb_server)

    for qitem in results:
        logger.debug("Starting to work on queue item %s" % qitem['id'])
        if qitem['type'] == "monitor":
            keyid = "monitor:" + qitem['item']['cid']

            # Delete
            # if Edit this will delete
            if qitem['action'] == "delete" or qitem['action'] == "edit":
                logger.debug("Initiating Monitor deletion for monitor id: %s" % qitem[
                    'item']['cid'])
                result = decimateRedis(keyid, qitem['item'])
                if result:
                    logger.info("Monitor %s removed redis queue" % qitem[
                        'item']['cid'])
                    if qitem['action'] == "delete":
                        delete = r.table(config['dbqueue']).get(
                            qitem['id']).delete().run(rdb_server)
                        if delete['deleted'] == 1:
                            logger.debug("Queue entry %s removed from RethinkDB queue" % qitem['id'])

            # Create
            # if Edit this will create
            if qitem['action'] == "create" or qitem['action'] == "edit":
                if "datacenter" not in qitem['item']['data']:
                    msg_format = "Initiating Monitor creation for monitor id: %s - no datacenter"
                    result = populateRedis(keyid, qitem['item'])
                else:
                    if config['dbqueue'] in qitem['item']['data']['datacenter']:
                        msg_format = "Initiating Monitor creation for monitor id: %s - local"
                        result = populateRedis(
                            keyid, qitem['item'], local=True)
                    else:
                        msg_format = "Initiating Monitor creation for monitor id: %s - notify"
                        result = populateRedis(keyid, qitem['item'])
                logger.debug(msg_format % qitem['item']['cid'])
                if result:
                    logger.info("Monitor %s added to redis queue" % qitem[
                        'item']['cid'])
                    delete = r.table(config['dbqueue']).get(
                        qitem['id']).delete().run(rdb_server)
                    if delete['deleted'] == 1:
                        logger.debug("Queue entry %s removed from RethinkDB queue" % qitem['id'])
                        status = r.table(
                            'monitors').get(qitem['item']['cid']).update(
                                {'status': 'monitored'}).run(rdb_server)
                        if status['replaced'] == 1:
                            logger.debug("Monitor %s status changed in RethinkDB" % qitem['item']['cid'])
                        else:
                            logger.debug("Failed to change monitor %s status in RethinkDB" % qitem['item']['cid'])
                else:
                    logger.debug("Skipping Monitor creation as it did not match datacenter checks: %s" % qitem['item']['cid'])
                    delete = r.table(config['dbqueue']).get(
                        qitem['id']).delete().run(rdb_server)
                    if delete['deleted'] == 1:
                        logger.debug("Queue entry %s removed from RethinkDB queue" % qitem['id'])

            # Sink messages
            # if Sink this will shoot a message to the actioner
            if qitem['action'] == "sink":
                logger.info("Got a web based health check from the queue, sending to sink")
                result = sendtoSink(qitem['item'])
                if result:
                    logger.info("Monitor %s sent to sink" % qitem['item']['cid'])
                    delete = r.table(config['dbqueue']).get(
                        qitem['id']).delete().run(rdb_server)
                    if delete['deleted'] == 1:
                        logger.debug("Queue entry %s removed from RethinkDB queue" % qitem['id'])

        # If Reaction
        if qitem['type'] == "reaction":
            keyid = "reaction:" + qitem['item']['rid']

            # Delete
            # if Edit this will delete
            if qitem['action'] == "delete" or qitem['action'] == "edit":
                logger.debug("Initiating Reaction deletion for reaction id: %s" % qitem['item']['rid'])
                result = decimateRedis(keyid, qitem['item'])
                if result:
                    logger.info("Reaction %s removed from redis" % qitem['item']['rid'])
                    delete = r.table(config['dbqueue']).get(
                        qitem['id']).delete().run(rdb_server)
                    if delete['deleted'] == 1:
                        logger.debug("Queue entry %s removed from RethinkDB queue" % qitem['id'])

            # Create
            # if Edit this will create
            if qitem['action'] == "create" or qitem['action'] == "edit":
                logger.debug("Initiating Reaction creation for reaction id: %s" % qitem['item']['rid'])
                result = populateRedis(keyid, qitem['item'])
                if result:
                    logger.info("Reaction %s added to redis" % qitem['item']['rid'])
                    delete = r.table(config['dbqueue']).get(
                        qitem['id']).delete().run(rdb_server)
                    if delete['deleted'] == 1:
                        logger.debug("Queue entry %s removed from RethinkDB queue" % qitem['id'])

    # Sleep for 10 seconds
    time.sleep(config['sleep'])
