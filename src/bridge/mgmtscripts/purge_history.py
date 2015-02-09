#!/usr/bin/python
#####################################################################
# Cloud Routes Management Scripts: Purge History
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This quicky designed to rebuild the redis queues from
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

from runbookdb import RunbookDB


# Load Configuration
# ------------------------------------------------------------------

if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

configfile = sys.argv[1]

with open(configfile, 'r') as cfh:
    config = yaml.safe_load(cfh)


# Open Config File and Parse Config Data
db=RunbookDB(configfile)
conn=db.connect()

# Open External Connections
# ------------------------------------------------------------------

# RethinkDB Server


# Helper Functions
# ------------------------------------------------------------------


# Execute
# ------------------------------------------------------------------

def purge_old_history():
    chktime = time.time() - config['history_retention']
    results = r.table('history').filter(
        (r.row['starttime'] < chktime)).delete().run(conn)


purge_old_history()

db.close()
