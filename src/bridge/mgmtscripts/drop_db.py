import sys
import yaml

import rethinkdb as r

from runbookdb import RunbookDB

if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]
with open(configfile, "r") as h:
    config = yaml.safe_load(h)


# Establish Connection
host = config['rethink_host']
database = config['rethink_db']


db=RunbookDB(configfile)
conn=db.connect()

# Drop Database
r.db_drop(database).run(conn)

print "Done!"
