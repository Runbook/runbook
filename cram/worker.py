#!/usr/bin/python
#####################################################################
## Cloud Routes Availability Manager: Worker
## ------------------------------------------------------------------
## Description:
## ------------------------------------------------------------------
## This is the worker process for the availability manager.
## This process checks for failure, if failure occurs than it will
## send a failure json message to the sink, on success it sends a
## successful message.
## ------------------------------------------------------------------
## Version: Alpha.20140424
## Original Author: Benjamin J. Cane - madflojo@cloudrout.es
## Contributors:
##  - your name here
#####################################################################


#### Imports
## ------------------------------------------------------------------

## Clean Paths for All
import sys
import zmq
from datetime import datetime
import syslog
import stathat
import yaml
import signal
import json
import time

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

## Startup ZeroMQ client 
context = zmq.Context()
zrecv = context.socket(zmq.PULL)
connectline = "tcp://%s:%d" % ( config['broker_ip'], config['broker_worker_port'] )
line = "Connecting to Broker at %s" % connectline
syslog.syslog(syslog.LOG_INFO, line)
zrecv.connect(connectline)

## Startup ZeroMQ push client
context2 = zmq.Context()
zsend = context2.socket(zmq.PUSH)
connectline = "tcp://%s:%d" % ( config['sink_ip'], config['sink_port'] )
line = "Connecting to Sink at %s" % connectline
syslog.syslog(syslog.LOG_INFO, line)
zsend.connect(connectline)

#### Handle Kill Signals Cleanly
## ------------------------------------------------------------------

def killhandle(signum, frame):
  ''' This will close connections cleanly '''
  line = "SIGTERM detected, shutting down"
  syslog.syslog(syslog.LOG_INFO, line)
  syslog.closelog()
  sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)


#### Create functions
## ------------------------------------------------------------------

def getTime():
  now = datetime.now()
  return now.strftime("%H:%M:%S.%f")


#### Do the work
## ------------------------------------------------------------------

## Give Broker time to wake up
time.sleep(5)

while True:
  jdata = zrecv.recv_json()
  # Log that we got a message
  stat = "[%s] Checks received by workers" % config['envname']
  stathat.ez_count(config['stathat_ez_key'], stat, 1)
  line = "Got message for monitor %s from broker" % jdata['cid']
  syslog.syslog(syslog.LOG_DEBUG, line)
  # Load health check module and run it
  monitor = __import__("checks." + jdata['ctype'], globals(), locals(), ['check'], -1)
  result = monitor.check(jdata)
  if result == True:
    # Log it
    stat = "[%s] Healthy Checks" % config['envname']
    stathat.ez_count(config['stathat_ez_key'], stat, 1)
    line = "Health check %s for monitor %s is Healthy" % (jdata['ctype'], jdata['cid'])
    syslog.syslog(syslog.LOG_INFO, line)
    jdata['check'] = {  'status': 'healthy',
                        'method': 'automatic' }
    # Send success to sink
    ztext = json.dumps(jdata)
  elif result == None:
    line = "Health check %s was unable to execute" % (jdata['cid'])
    syslog.syslog(syslog.LOG_ERR, line)
    ztext = None
  else:
    # Log it
    stat = "[%s] Failed Checks" % config['envname']
    stathat.ez_count(config['stathat_ez_key'], stat, 1)
    line = "Health check %s for monitor %s is Failed" % (jdata['ctype'], jdata['cid'])
    syslog.syslog(syslog.LOG_INFO, line)
    jdata['check'] = {  'status': 'failed',
                        'method': 'automatic' }
    jdata['time_tracking']['worker'] = time.time()
    # Send success to sink
    ztext = json.dumps(jdata)

  # Send data to sink and log it
  if ztext is not None:
    zsend.send(ztext)
    stat = "[%s] Checks sent to sink from workers" % config['envname']
    stathat.ez_count(config['stathat_ez_key'], stat, 1)
    line = "Health check %s sent to sink" % jdata['cid']
    syslog.syslog(syslog.LOG_INFO, line)
