#!/usr/bin/python
#####################################################################
# Cloud Routes Bridge: Broker
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is a message broker for the actioner.
# This process will get messages from the various monitor processes
# and send them to the actioner worker processes via zMQ.
# ------------------------------------------------------------------
# Original Author: Benjamin J. Cane - @madflojo
# Maintainers:
# - Benjamin Cane - @madflojo
#####################################################################


# Imports
# ------------------------------------------------------------------

import sys
import zmq
import time
import yaml
import signal
import logconfig

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
logger = logconfig.getLogger('crbridge.broker', config['use_syslog'])

logger.info("Using config %s" % configfile)

# Start ZeroMQ listener for control
context = zmq.Context()
zrecv = context.socket(zmq.PULL)
bindaddress_pull = "tcp://%s:%d" % (config['sink_ip'], config['sink_port'])
zrecv.bind(bindaddress_pull)
logger.info("Attempting to bind to %s for pulling" % bindaddress_pull)

# Start ZeroMQ listener for workers
context2 = zmq.Context()
zsend = context2.socket(zmq.PUSH)
bindaddress_push = "tcp://%s:%d" % (
    config['sink_ip'], config['sink_worker_port'])
zsend.bind(bindaddress_push)
logger.info("Attempting to bind to %s for pushing" % bindaddress_push)


# Handle Kill Signals Cleanly
# ------------------------------------------------------------------

def killhandle(signum, frame):
    ''' This will close connections cleanly '''
    logger.info("SIGTERM detected, shutting down")
    zsend.close()
    zrecv.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)


# Run For Loop
# ------------------------------------------------------------------

# Let the workers get started
time.sleep(20)

# Start an infinante loop that checks every 2 minutes
while True:
    # Get list of members to check from queue
    msg = zrecv.recv()
    logger.debug("Got message from %s, sending it to %s, %s" % (
        bindaddress_pull, bindaddress_push, msg))
    zsend.send(msg)

    # The following should be disabled unless it is times of distress
    #import json
    #jdata = json.loads(msg)
    #logger.debug("Sent health check %s to workers" % jdata['cid'])
