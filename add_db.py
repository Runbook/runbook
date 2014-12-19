# add_db.py


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

    userdata = {
        'username': 'test@tester.com',
        'email': 'test@tester.com',
        'password': 'password456',
        'company': 'company',
        'contact': 'tester'
    }

    # add dummy user
    r.db(database).table('users').insert([userdata]).run(conn)

    # output data
    cursor = r.db(database).table('users').run(conn)
    for user in cursor:
        print user

    # remove data
    r.db(database).table('users').delete().run(conn)

    # close connection
    conn.close()

    print "Done!"
