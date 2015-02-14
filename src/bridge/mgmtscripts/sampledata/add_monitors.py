import sys
import yaml
import time

from werkzeug.security import generate_password_hash
import rethinkdb as r

from rethinkdb.errors import RqlRuntimeError, RqlDriverError

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
database = config['rethink_db']

try:
    if config['rethink_authkey']:
        conn = r.connect(
            host=config['rethink_host'], port=config['rethink_port'],
            auth_key=config['rethink_authkey'], db=config['rethink_db']).repl()
    else:
        conn = r.connect(
            host=config['rethink_host'], port=config['rethink_port'],
            db=config['rethink_db']).repl()
    print "Connecting to RethinkDB"
except RqlDriverError:
    print "Cannot connect to rethinkdb, shutting down"
    sys.exit(1)


uid = 'b21f2ac2-bad9-4552-a059-064c91c474e9'

monitordata = {
    'ctype':  'http-get-statuscode' ,
    'data': {
        'codes': [
            '200'
            ] ,
        'datacenter': [
            'dc1queue'
            ] ,
        'host':  'runbook.io' ,
        'name':  'my_monitor' ,
        'reactions': [ ],
        'timer':  '2mincheck' , # 30seccheck 
        'url': 'http://runbook.io', 
        } ,
    'failcount': 2 ,
    'id':  '777a6af7-4c24-46cf-b4c2-5e8bad9c8dc5' ,
    'name':  'my_monitor' ,
    'status':  'true' ,
    'uid':  uid ,
    'url':  'WyI3NzdhNmFmNy00YzI0LTQ2Y2YtYjRjMi01ZThiYWQ5YzhkYzUiXQ.YU5FLBsP-l44cPHipuxh1A_AZGU'
    }


userdata = {
    'id':  'b21f2ac2-bad9-4552-a059-064c91c474e9' ,
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
r.db(database).table('monitors').insert([monitordata]).run(conn)

# Output Data
cursor = r.db(database).table('monitors').run(conn)
for user in cursor:
    print user

# Remove Data
# r.db(database).table('users').delete().run(conn)

# Close Connection
conn.close()

print 'Sample Monitor Added!'
