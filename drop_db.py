import sys
import os

import rethinkdb as r
from rethinkdb.errors import RqlDriverError, RqlRuntimeError

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
    r.db_drop(database).run(conn)
    print "Done!"
