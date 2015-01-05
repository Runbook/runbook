#!/usr/bin/env python
#####################################################################
# Cloud Routes Management Scripts: Purge Events
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is designed to remove anything from the events
# table exceeding the 'events_retention' threshold set within the
# bridge config.
# ------------------------------------------------------------------
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
with open(configfile, 'r') as cfh:
    config = yaml.safe_load(cfh)


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

chktime = time.time() - config['events_retention']
results = r.table('events').filter(
    (r.row['time'] < chktime)).delete().run(rdb_server)
