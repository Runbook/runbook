import sys
import yaml

import rethinkdb as r

if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]
cfh = open(configfile, "r")
config = yaml.safe_load(cfh)
cfh.close()

# Establish Connection
host = config['rethink_host']
database = config['rethink_db']
auth_key = config['rethink_authkey']
conn = r.connect(host, 28015, auth_key=auth_key).repl()

# Create Database and Tables
r.db_create(database).run(conn)
r.db(database).table_create('monitors').run(conn)
r.db(database).table_create('reactions').run(conn)
r.db(database).table_create('users').run(conn)
r.db(database).table_create('history').run(conn)
r.db(database).table_create('events').run(conn)
r.db(database).table_create('subscription_history').run(conn)
r.db(database).table_create('dc1queue').run(conn)
r.db(database).table_create('dc2queue').run(conn)

print "Done!"


#######################
### Database Tables ###
#######################

"""
monitors - Stores monitors
reactions - Stores reactions
users - Stores user data
history - Stores historical tracking for monitors and reactions
events - Stores unique events for monitors
subscription_history - Stores subscription history for tracking signups
dc1queue - Queue for monitors and reactions in datacenter 1
dc2queue - Queue for monitors and reactions in datacenter 2
"""
