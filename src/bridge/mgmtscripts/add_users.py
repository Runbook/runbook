import sys
import yaml
import time

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

userdata = {
    'username': 'test@tester.com',
    'password': 'password456321',
    'email': 'test@tester.com',
    'status': 'active',
    'company': 'runbook',
    'contact': 'tester',
    'acttype': 'lite-v2',
    'creation_time': time.time(),
    'confirmed': True
}

# Add Dummy User
r.db(database).table('users').insert([userdata]).run(conn)

# Output Data
cursor = r.db(database).table('users').run(conn)
for user in cursor:
    print user

# Remove Data
# r.db(database).table('users').delete().run(conn)

# Close Connection
conn.close()

print "User Added!"
