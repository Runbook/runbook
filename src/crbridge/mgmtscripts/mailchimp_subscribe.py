#!/usr/bin/python
#####################################################################
# Cloud Routes Management Scripts: Mailchimp subscribe
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# Pull newly created users from the database and automatically
# subscribe them to the MailChimp mailing list.
# ------------------------------------------------------------------
# Version: Alpha.20140813
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - Paul Deardorff (themetric)
#####################################################################


# Imports
# ------------------------------------------------------------------

# Clean Paths for All
import sys
import yaml
import rethinkdb as r
from rethinkdb.errors import RqlDriverError
from requests import post
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
# TODO move default connection into module
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

emails_to_subscribe = []
results = r.table('users').filter({subscribed_to_newsletter: False}).run(rdb_server)
for user in results:
    print("Found new user: %s") % user['email']
    emails_to_subscribe.append(user['email'])
if len(emails_to_subscribe) > 0:
    print("Subscribing %s emails to MailChimp...") % len(emails_to_subscribe)
    data = json.dumps({
      "apikey": config['mailchimp_api_key'], # in the form XXX-us2
      "id": config['mailchimp_api_key'], # in the form a23o9af0f
      "batch": [{"email": {"email": email}} for email in emails_to_subscribe]
    })
    resp = post(
      "https://us2.api.mailchimp.com/2.0/lists/batch-subscribe",
      data=data,
      headers={'Content-type': 'application/json'}
    ).json()
    if "add_count" in resp:
      print("%s email(s) successfully subscribed!") % resp["add_count"]
      # For each user successfully subscribed,
      # update the user with subscribed_to_newsletter = True
    else:
      print resp
else:
    print("No email(s) to send to MailChimp list.")
