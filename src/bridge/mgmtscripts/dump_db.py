import sys
import yaml
import time
import pprint 

from werkzeug.security import generate_password_hash
import rethinkdb as r

from runbookdb import RunbookDB

if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]
with open(configfile, "r") as cfh:
    config = yaml.safe_load(cfh)


# Establish Connection
database = config['rethink_db']

db=RunbookDB(configfile)
conn=db.connect()


tables = {
    "dc1queue" ,
    "dc2queue" ,
    "events" ,
    "history" ,
    "reactions" ,
    "subscription_history" ,
    "users",
    }

for table in tables:
    print "==========TABLE %s" % table
    cursor = r.db(database).table(table).run(conn)
    for row in cursor:
        pprint.pprint(row, width=1)
    print "================================================================"
    print 

# Close Connection
db.close()

print 'DB Dump Complete!'
