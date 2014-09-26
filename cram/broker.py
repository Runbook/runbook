#!/usr/bin/python
#####################################################################
## Cloud Routes Availability Manager: Broker
## ------------------------------------------------------------------
## Description:
## ------------------------------------------------------------------
## This is a message broker for the availability manager.
## This process will send messages from the various control processes
## and send them to the worker processes via zMQ.
## ------------------------------------------------------------------
## Version: Alpha.20140308
## Original Author: Benjamin J. Cane - madflojo@cloudrout.es
## Contributors:
##  - your name here
#####################################################################


#### Imports
## ------------------------------------------------------------------

import sys
import zmq
import time
import yaml
import signal
import syslog

#### Load Configuration
## ------------------------------------------------------------------

if len(sys.argv) != 2:
  print("Hey, thats not how you launch this...")
  print("%s <config file>") % sys.argv[0]
  sys.exit(1)

## Open Config File and Parse Config Data
configfile = sys.argv[1]
cfh = open(configfile, "r")
config = yaml.safe_load(cfh)
cfh.close()


#### Make Connections
## ------------------------------------------------------------------

## Open Syslog
syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL0)

## Start ZeroMQ listener for control
context = zmq.Context()
zrecv = context.socket(zmq.PULL)
bindaddress = "tcp://%s:%d" % ( config['broker_ip'], config['broker_control_port'] )
zrecv.bind(bindaddress)
line = "Attempting to bind to %s" % bindaddress
syslog.syslog(syslog.LOG_INFO, line)

## Start ZeroMQ listener for workers
context2 = zmq.Context()
zsend = context2.socket(zmq.PUSH)
bindaddress = "tcp://%s:%d" % ( config['broker_ip'], config['broker_worker_port'] )
zsend.bind(bindaddress)
line = "Attempting to bind to %s" % bindaddress
syslog.syslog(syslog.LOG_INFO, line)


#### Handle Kill Signals Cleanly
## ------------------------------------------------------------------

def killhandle(signum, frame):
  ''' This will close connections cleanly '''
  line = "SIGTERM detected, shutting down"
  syslog.syslog(syslog.LOG_INFO, line)
  syslog.closelog()
  zsend.close()
  zrecv.close()
  sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)


#### Run For Loop
## ------------------------------------------------------------------

## Let the workers get started
time.sleep(20)

## Start an infinante loop that checks every 2 minutes
while True:
  # Get list of members to check from queue
  msg = zrecv.recv()
  line = "Got the following message and sent it off %s" % msg
  syslog.syslog(syslog.LOG_DEBUG, line)
  zsend.send(msg)

  # The following should be disabled unless it is times of distress 
  #import json
  #jdata = json.loads(msg)
  #line = "Sent health check %s to workers" % jdata['cid']
  #syslog.syslog(syslog.LOG_DEBUG, line)
