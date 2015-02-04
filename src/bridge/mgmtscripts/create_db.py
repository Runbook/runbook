import sys
import yaml

import rethinkdb as r
from rethinkdb.errors import RqlDriverError, RqlRuntimeError
import socket

def createTable(dbname, tablename, conn):
    ''' Create a rethinkDB table '''
    print("Creating table: %s") % tablename
    try:
        r.db(dbname).table_create(tablename).run(conn)
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        print("RethinkDB Error: %s") % e.message
        print("Table %s not created") % tablename

if len(sys.argv) < 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file> [--travis]") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]
cfh = open(configfile, "r")
config = yaml.safe_load(cfh)
cfh.close()

if sys.argv[2] 
    if sys.argv[2] == "--travis":
      travis = True
    else:
      print("Didn't understand second command line argument.."
            "Assuming non-Travis environment")

# Establish Connection
host = config['rethink_host']
port = config['rethink_port']
database = config['rethink_db']
auth_key = config['rethink_authkey']
try:
    if auth_key && travis == False:
        conn = r.connect(host, port, auth_key=auth_key).repl()
    else:
        conn = r.connect(host, port).repl()
except (RqlDriverError, RqlRuntimeError, socket.error) as e:
    print("RethinkDB Error on Connection: %s") % e.message
    sys.exit(1)

if travis == True:
    try:
        r.db('rethinkdb').table('cluster_config').get('auth').update({ 'auth_key' : auth_key }).run(conn)
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        print("RethinkDB Error setting auth key: %s") % e.message

result = r.db_list().run(conn)
if database in result:
    print("Database %s already exists exiting") % database
    sys.exit(0)

r.db_create(database).run(conn)
tables = [
    'monitors',
    'reactions',
    'users',
    'history',
    'events',
    'subscription_history',
    'dc1queue',
    'dc2queue'
]
for name in tables:
    createTable(database, name, conn)
print "Database created!"


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
