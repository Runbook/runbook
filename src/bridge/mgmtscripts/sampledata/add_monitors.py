import sys
import yaml
import time

from werkzeug.security import generate_password_hash
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
database = config['rethink_db']

db=RunbookDB(configfile)
conn=db.connect()


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
        'reactions': [ 'rid_1' ],
        'timer':  '2mincheck' , # 30seccheck 
        'url': 'http://runbook.io', 
        } ,
    'failcount': 2 ,
    'id':  'mid_1' ,
    'name':  'my_monitor' ,
    'status':  'true' ,
    'uid':  'uid_1' ,
    'url':  'WyI3NzdhNmFmNy00YzI0LTQ2Y2YtYjRjMi01ZThiYWQ5YzhkYzUiXQ.YU5FLBsP-l44cPHipuxh1A_AZGU'
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
