#!/usr/bin/python
#####################################################################
# Cloud Routes Management Scripts: Mailchimp subscribe
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
from rethinkdb.errors import RqlDriverError
from requests import post
import json

# Load Configuration
# ------------------------------------------------------------------

if len(sys.argv) < 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file> [--refresh]") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]
cfh = open(configfile, "r")
config = yaml.safe_load(cfh)
cfh.close()

# Parse command line option
# Refresh will set all users subscribed_to_newsletter = False
refresh_users = (len(sys.argv) > 2 and sys.argv[2] == "--refresh")

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

# If the command option --refresh is added,
# then re-subscribe all users to Mailchimp
if refresh_users:
    r.table('users').update({"subscribed_to_newsletter": False}).run(rdb_server)

results = r.table('users').filter({"subscribed_to_newsletter": False}).run(rdb_server)
for user in results:
    print("Found new user: %s") % user['email']
    emails_to_subscribe.append(user['email'])
if len(emails_to_subscribe) > 0:
    print("Subscribing %s email(s) to MailChimp...") % len(emails_to_subscribe)
    data = json.dumps({
        "apikey": config['mailchimp_api_key'], # in the form XXX-us2
        "id": config['mailchimp_list_id'], # in the form a23o9af0f
        "double_optin": False,
        "batch": [{"email": {"email": email}} for email in emails_to_subscribe]
    })
    url = config['mailchimp_api_url'] + "/lists/batch-subscribe"
    resp = post(
        url=url,
        data=data,
        headers={'Content-type': 'application/json'}
    ).json()
    if "add_count" in resp:
        print("%s email(s) successfully subscribed!") % resp["add_count"]
        print("%s email(s) false subscription!") % resp["error_count"]
        for subscribed in resp["adds"]:
            r.table("users").filter({"email": subscribed["email"]}).update({"subscribed_to_newsletter": True}).run(rdb_server)
        if int(resp["add_count"]) == 0 and int(resp["error_count"]) > 1:
            sys.exit(1)
    else:
        print resp
else:
    print("No email(s) to send to MailChimp list.")
