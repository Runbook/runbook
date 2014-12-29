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

# Drop Database
r.db_drop(database).run(conn)

print "Done!"
