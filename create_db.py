# create_db.py


import sys
import os

import rethinkdb as r

from flask import Flask

configfile = os.path.join('src', 'web', 'instance', 'web.cfg')
if len(sys.argv) > 1:
    configfile = sys.argv[1]
print("Using config %s" % configfile)


app = Flask("createdb")
if app.config.from_pyfile(configfile):
    host = app.config['DBHOST']
    database = app.config['DATABASE']
    auth_key = app.config['DBAUTHKEY']
    conn = r.connect(host, 28015, auth_key=auth_key).repl()

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
