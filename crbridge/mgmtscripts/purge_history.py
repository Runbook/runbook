#!/usr/bin/python
#####################################################################
# Cloud Routes Management Scripts: Purge History
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is a semi quicky designed to rebuild the redis queues from
# the RethinkDB database
# ------------------------------------------------------------------
# Version: Alpha.20140729
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

# RethinkDB Server
try:
    rdb_server = r.connect(
        host=config['rethink_host'], port=config['rethink_port'],
        auth_key=config['rethink_authkey'], db=config['rethink_db'])
    line = "Connecting to RethinkDB"
    print line
except RqlDriverError:
    line = "Cannot connect to rethinkdb, shutting down"
    print line
    sys.exit(1)

# Helper Functions
# ------------------------------------------------------------------


# Execute
# ------------------------------------------------------------------

chktime = time.time() - config['history_retention']
results = r.table('history').filter(
    (r.row['starttime'] < chktime)).delete().run(rdb_server)
