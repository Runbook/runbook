#!/usr/bin/python
#####################################################################
# Cloud Routes Management Scripts: Get Stats
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# Pull newly created users from the database and automatically
# subscribe them to the MailChimp mailing list.
# ------------------------------------------------------------------
# Original Author: Paul Deardorff (themetric)
# Maintainers:
# - Paul Deardorff (themetric)
# - Benjamin Cane (madflojo)
#####################################################################


# Imports
# ------------------------------------------------------------------

# Clean Paths for All
import sys
import yaml
import rethinkdb as r
from rethinkdb.errors import RqlDriverError, RqlRuntimeError
import requests
import json
import pprint

from runbookdb import RunbookDB

# Load Configuration
# ------------------------------------------------------------------

if len(sys.argv) < 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

configfile = sys.argv[1]

with open(configfile, 'r') as cfh:
    config = yaml.safe_load(cfh)

# Open External Connections
# ------------------------------------------------------------------

# RethinkDB Server
# [DONE] TODO move default connection into module
db=RunbookDB(configfile)
conn=db.connect()

# Helper Functions
# ------------------------------------------------------------------


# Run For Loop
# ------------------------------------------------------------------

msg = {
    "ezkey" : config['stathat_key'],
    "data" : []
}

# Get user count
try:
    result = r.table('users').count().run(conn)
except (RqlDriverError, RqlRuntimeError) as e:
    print("Got error while performing query: %s") % e.message
    print("Exiting...")
    sys.exit(1)

msg['data'].append({
    'stat' : "[%s] Total Users" % config['envname'],
    "value" : result
})


# Get upgraded user count and monitor count
try:
    result = r.table('users').filter({'acttype': 'pro'}).run(conn)
except (RqlDriverError, RqlRuntimeError) as e:
    print("Got error while performing query: %s") % e.message
    print("Exiting...")
    sys.exit(1)

total_up_users = {
    'monthly' : 0,
    'yearly' : 0,
    'total' : 0
} 
total_up_mons = {
    'monthly' : 0,
    'yearly' : 0,
    'total' : 0
} 

for user in result:
    total_up_users['total'] = total_up_users['total'] + 1
    total_up_mons['total'] = total_up_mons['total'] + user['subplans']
    if "monthly" in user['subscription']:
        total_up_users['monthly'] = total_up_users['monthly'] + 1
        total_up_mons['monthly'] = total_up_mons['monthly'] + user['subplans']
    elif "yearly" in user['subscription']:
        total_up_users['yearly'] = total_up_users['yearly'] + 1
        total_up_mons['yearly'] = total_up_mons['yearly'] + user['subplans']

msg['data'].append({
    'stat' : "[%s] Total Upgraded Users" % config['envname'],
    "value" : total_up_users['total']
})
msg['data'].append({
    'stat' : "[%s] Total Purchased Monitors" % config['envname'],
    "value" : total_up_mons['total']
})


msg['data'].append({
    'stat' : "[%s] Total Upgraded Users - Monthly Subscription" % config['envname'],
    "value" : total_up_users['monthly']
})
msg['data'].append({
    'stat' : "[%s] Total Purchased Monitors - Monthly Subscription" % config['envname'],
    "value" : total_up_mons['monthly']
})

msg['data'].append({
    'stat' : "[%s] Total Upgraded Users - Yearly Subscription" % config['envname'],
    "value" : total_up_users['yearly']
})
msg['data'].append({
    'stat' : "[%s] Total Purchased Monitors - Yearly Subscription" % config['envname'],
    "value" : total_up_mons['yearly']
})

# Get monitor count
try:
    result = r.table('monitors').count().run(conn)
except (RqlDriverError, RqlRuntimeError) as e:
    print("Got error while performing query: %s") % e.message
    print("Exiting...")
    sys.exit(1)

msg['data'].append({
    'stat' : "[%s] Total Monitors" % config['envname'],
    "value" : result
})


# Get reaction count
try:
    result = r.table('reactions').count().run(conn)
except (RqlDriverError, RqlRuntimeError) as e:
    print("Got error while performing query: %s") % e.message
    print("Exiting...")
    sys.exit(1)

msg['data'].append({
    'stat' : "[%s] Total Reactions" % config['envname'],
    "value" : result
})

pprint.pprint(msg)
payload = json.dumps(msg)
headers = { 'Content-Type': 'application/json' }

req = requests.post(url="http://api.stathat.com/ez", headers=headers, data=payload)
if req.status_code >= 200 and req.status_code <= 299:
    print("Successfully sent stats to stathat")
