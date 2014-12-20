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
# Version: Alpha.20140306
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
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
import syslog


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
    line = "Connecting to redis"
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
    line = "Connecting to RethinkDB"
    syslog.syslog(syslog.LOG_INFO, line)
except RqlDriverError:
    line = "Cannot connect to rethinkdb, shutting down"
    syslog.syslog(syslog.LOG_ERR, line)
    sys.exit(1)

# Handle Kill Signals Cleanly
# ------------------------------------------------------------------


def killhandle(signum, frame):
    ''' This will close connections cleanly '''
    line = "SIGTERM detected, shutting down"
    syslog.syslog(syslog.LOG_INFO, line)
    rdb_server.close()
    # zsend.close()  # zsend?
    syslog.closelog()
    sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)


# Helper Functions
# ------------------------------------------------------------------


# Run For Loop
# ------------------------------------------------------------------

users = r.table('users').run(rdb_server)
for user in users:
    r.table('users').get(user['id']).update(
        {'confirmed': True}
    ).run(rdb_server)
