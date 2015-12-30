#!/usr/bin/python
#####################################################################
# Cloud Routes Management Scripts: Decimate Redis
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is a quicky designed to remove all redis keys
# ------------------------------------------------------------------
# Version: Alpha.20140813
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
#####################################################################


# Imports
# ------------------------------------------------------------------

# Clean Paths for All
import sys
import yaml
import redis


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

# Redis Server
try:
    r_server = redis.Redis(
        host=config['redis_host'], port=config['redis_port'],
        db=config['redis_db'], password=config['redis_password'])
    line = "Connecting to redis"
    print(line)
except:
    line = "Cannot connect to redis, shutting down"
    print(line)
    sys.exit(1)


# Helper Functions
# ------------------------------------------------------------------


# Run For Loop
# ------------------------------------------------------------------

keys = r_server.keys("*")
for key in keys:
    print("Removing key: %s") % key
    r_server.delete(key)

## Extra good measure
r_server.flushdb()
