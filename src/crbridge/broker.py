#!/usr/bin/python
#####################################################################
# Cloud Routes Bridge: Broker
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is a message broker for the actioner.
# This process will get messages from the various cram processes
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
logger = logconfig.getLogger('crbridge.broker')

# Start ZeroMQ listener for control
context = zmq.Context()
zrecv = context.socket(zmq.PULL)
bindaddress = "tcp://%s:%d" % (config['sink_ip'],
                               config['sink_port'])
zrecv.bind(bindaddress)
logger.info("Attempting to bind to %s" % bindaddress)

# Start ZeroMQ listener for workers
context2 = zmq.Context()
zsend = context2.socket(zmq.PUSH)
bindaddress = "tcp://%s:%d" % (config['sink_ip'],
                               config['sink_worker_port'])
zsend.bind(bindaddress)
logger.info("Attempting to bind to %s" % bindaddress)


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
    logger.debug("Got the following message and sent it off %s" % msg)
    zsend.send(msg)

    # The following should be disabled unless it is times of distress
    #import json
    #jdata = json.loads(msg)
    #logger.debug("Sent health check %s to workers" % jdata['cid'])
