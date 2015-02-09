import sys
import yaml
import time

from werkzeug.security import generate_password_hash
import rethinkdb as r

from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from runbookdb import RunbookDB


if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

configfile = sys.argv[1]

with open(configfile, 'r') as cfh:
    config = yaml.safe_load(cfh)


# Open Config File and Parse Config Data
db=RunbookDB(configfile)
conn=db.connect()


# Establish Connection
database = config['rethink_db']

userdata = {
    'username': 'test@tester.com',
    'password': generate_password_hash('password456321'),
    'email': 'test@tester.com',
    'status': 'active',
    'company': 'runbook',
    'contact': 'tester',
    'acttype': 'lite-v2',
    'creation_time': time.time(),
    'confirmed': True,
    'stripe': None,
    'stripeid': None ,
    'subplans': 2 ,
    'subscribed_to_newsletter': False ,
    'subscription':  'Free' ,
}

# Add Dummy User
r.db(database).table('users').insert([userdata]).run(conn)

# Output Data
cursor = r.db(database).table('users').run(conn)
for user in cursor:
    print user

# Remove Data
#r.db(database).table('users').delete().run(conn)

# Close Connection
conn.close()

print "User Added!"
