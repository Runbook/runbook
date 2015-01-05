#!/usr/bin/python
#####################################################################
# Cloud Routes Management Scripts: Rebuild Redis
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is designed to rebuild the redis queues from the RethinkDB
# database
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
import json


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
    rdb_server = r.connect(host=config[
        'rethink_host'], port=config['rethink_port'],
        auth_key=config['rethink_authkey'], db=config['rethink_db'])
    line = "Connecting to RethinkDB"
    print line
except RqlDriverError:
    line = "Cannot connect to rethinkdb, shutting down"
    print line
    sys.exit(1)

# Helper Functions
# ------------------------------------------------------------------


# Run For Loop
# ------------------------------------------------------------------

results = r.table('monitors').run(rdb_server)
for item in results:
    print("Grabbing info for monitor: %s") % item['id']
    qdata = {'item': {
        'name': item['name'],
        'ctype': item['ctype'],
        'uid': item['uid'],
        'url': item['url'],
        'failcount': item['failcount'],
        'status': item['status'],
        'data': item['data']}
    }
    qdata['action'] = 'edit'
    qdata['type'] = 'monitor'
    qdata['item']['cid'] = item['id']

    for dc in ["dc1queue", "dc2queue"]:
        print("Sending to %s: %s") % (dc, json.dumps(qdata))
        q1 = r.table(dc).insert(qdata).run(rdb_server)


results = r.table('reactions').run(rdb_server)
for item in results:
    print("Grabbing info for reaction: %s") % item['id']
    qdata = {'item': {
        'name': item['name'],
        'rtype': item['rtype'],
        'uid': item['uid'],
        'trigger': item['trigger'],
        'frequency': item['frequency'],
        'lastrun': item['lastrun'],
        'data': item['data']}
    }
    qdata['action'] = 'edit'
    qdata['type'] = 'reaction'
    qdata['item']['rid'] = item['id']

    for dc in ["dc1queue", "dc2queue"]:
        print("Sending to %s: %s") % (dc, json.dumps(qdata))
        q1 = r.table(dc).insert(qdata).run(rdb_server)
