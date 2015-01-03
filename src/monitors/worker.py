#!/usr/bin/python
#####################################################################
# Cloud Routes Availability Manager: Worker
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is the worker process for the availability manager.
# This process checks for failure, if failure occurs than it will
# send a failure json message to the sink, on success it sends a
# successful message.
# ------------------------------------------------------------------
# Original Author: Benjamin J. Cane - @madflojo
# Maintainers:
# - Benjamin Cane - @madflojo
#####################################################################


# Imports
# ------------------------------------------------------------------

# Clean Paths for All
import sys
import zmq
from datetime import datetime
import logconfig
import stathat
import yaml
import signal
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


# Make Connections
# ------------------------------------------------------------------

# Init logger
logger = logconfig.getLogger('monitors.worker', config['use_syslog'])

logger.info("Using config %s" % configfile)

# Startup ZeroMQ client
context = zmq.Context()
zrecv = context.socket(zmq.PULL)
connectline = "tcp://%s:%d" % (config['broker_ip'],
                               config['broker_worker_port'])
logger.info("Connecting to Broker at %s" % connectline)
zrecv.connect(connectline)

# Startup ZeroMQ push client
context2 = zmq.Context()
zsend = context2.socket(zmq.PUSH)
connectline = "tcp://%s:%d" % (config['sink_ip'], config['sink_port'])
logger.info("Connecting to Sink at %s" % connectline)
zsend.connect(connectline)

# Handle Kill Signals Cleanly
# ------------------------------------------------------------------


def killhandle(signum, frame):
    ''' This will close connections cleanly '''
    logger.info("SIGTERM detected, shutting down")
    sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)


# Create functions
# ------------------------------------------------------------------

def getTime():
    now = datetime.now()
    return now.strftime("%H:%M:%S.%f")


# Do the work
# ------------------------------------------------------------------

# Give Broker time to wake up
time.sleep(5)

while True:
    jdata = zrecv.recv_json()
    # Log that we got a message
    stat = "[%s] Checks received by workers" % config['envname']
    stathat.ez_count(config['stathat_ez_key'], stat, 1)
    logger.debug("Got message for monitor %s from broker" % jdata['cid'])
    # Load health check module and run it
    monitor = __import__(
        "checks." + jdata['ctype'], globals(), locals(), ['check'], -1)
    result = monitor.check(jdata=jdata)
    if result is True:
        # Log it
        stat = "[%s] True Checks" % config['envname']
        stathat.ez_count(config['stathat_ez_key'], stat, 1)
        logger.info("Health check %s for monitor %s is True" % (
            jdata['ctype'], jdata['cid']))
        jdata['check'] = {'status': 'true',
                          'method': 'automatic'}
        jdata['time_tracking']['worker'] = time.time()
        # Send success to sink
        ztext = json.dumps(jdata)
    elif result is None:
        logger.error("Health check %s was unable to execute" % (jdata['cid']))
        ztext = None
    else:
        # Log it
        stat = "[%s] False Checks" % config['envname']
        stathat.ez_count(config['stathat_ez_key'], stat, 1)
        logger.info("Health check %s for monitor %s is False" % (
            jdata['ctype'], jdata['cid']))
        jdata['check'] = {'status': 'false',
                          'method': 'automatic'}
        jdata['time_tracking']['worker'] = time.time()
        # Send success to sink
        ztext = json.dumps(jdata)

    # Send data to sink and log it
    if ztext is not None:
        zsend.send(ztext)
        stat = "[%s] Checks sent to sink from workers" % config['envname']
        stathat.ez_count(config['stathat_ez_key'], stat, 1)
        logger.info("Health check %s sent to sink" % jdata['cid'])
