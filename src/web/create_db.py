# create_db.py


import sys
import os

import rethinkdb as r
from rethinkdb.errors import RqlDriverError, RqlRuntimeError
import socket

from flask import Flask

configfile = os.path.join('src', 'web', 'instance', 'web.cfg')
if len(sys.argv) > 1:
    configfile = sys.argv[1]
print("Using config %s" % configfile)

def createTable(dbname, tablename, conn):
    ''' Create a rethinkDB table '''
    try:
        r.db(dbname).table_create(tablename).run(conn)
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        print("RethinkDB Error: %s") % e.message
        print("Table %s not created") % tablename


app = Flask("createdb")
if app.config.from_pyfile(configfile):
    host = app.config['DBHOST']
    database = app.config['DATABASE']
    port = app.config['DBPORT']
    print("Connecting to %s:%s") % (host, port)
    auth_key = app.config['DBAUTHKEY']
    try:
        if auth_key:
            conn = r.connect(host, port, auth_key=auth_key).repl()
        else:
            conn = r.connect(host, port).repl()
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        print("RethinkDB Error on Connection: %s") % e.message
        sys.exit(1)

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
