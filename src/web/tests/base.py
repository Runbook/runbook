######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - base
######################################################################


import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, abort
from flask.ext.testing import TestCase

from web import app
from users import User


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        return app

    def setUp(self):
        try:
            g.rdb_conn = r.connect(
                host=app.config['DBHOST'], port=app.config['DBPORT'],
                auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])

            userdata = {
                'username': 'test@tester.com',
                'email': 'test@tester.com',
                'password': 'password456',
                'company': 'company',
                'contact': 'tester'
            }

            # Create test user
            user = User()
            user.config = app.config
            user.createUser(userdata, g.rdb_conn)

        except RqlDriverError:
            # If no connection possible throw 503 error
            abort(503, "No Database Connection Could be Established.")

    def tearDown(self):
        # why the need to reconnect?
        g.rdb_conn = r.connect(
            host=app.config['DBHOST'], port=app.config['DBPORT'],
            auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])
        r.db('crdb').table('users').delete().run(g.rdb_conn)
        try:
            g.rdb_conn.close()
        except AttributeError:
            # Who cares?
            pass
