#!/usr/bin/python
#####################################################################
# Cloud Routes Web Application
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is the meat and potatoes of cloudrout.es. This will be the
# web based UI for users to login and manage domains and health
# checks. Any static pages are generated via genpages.py, this
# application was written with the use of Flask and is only for
# dynamic content.
# ------------------------------------------------------------------
# Version: Alpha.20140301
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
#####################################################################

# Imports (pre-app creation)
# ------------------------------------------------------------------

# Misc. Python goodies
import os
import sys
import cookies

# Flask modules
from flask import Flask
from flask import render_template
from flask import abort
from flask import g

# Scalable Database
import rethinkdb as r
from rethinkdb.errors import RqlDriverError


# Application Configuration
# ------------------------------------------------------------------

app = Flask(__name__)
# Config files are located in the instance directory
configfile = os.path.join('instance', 'crweb.cfg')
if len(sys.argv) > 1:
    configfile = sys.argv[1]
print("Using config %s" % configfile)
app.config.from_pyfile(configfile)


# Common Functions
# ------------------------------------------------------------------

def verifyLogin(secretkey, mxtime, cookdata):
    ''' This verifies the cookie being sent from the browser '''
    string = cookdata.get('loggedin')
    uid = cookies.verifyCdata(string, secretkey, mxtime)
    return uid


def startData(user=None):
    ''' This will set some common parameters for the data dictionary '''
    data = {}
    if user:
        data['status'] = user.status
        data['company'] = user.company
        data['loggedin'] = True
        if user.acttype == "lite" or user.acttype == "free":
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes')]
            data['limit'] = 10
            data['rlimit'] = 50
            data['dataret'] = 86400
            data['acttype'] = "Lite"
            data['cost'] = "Free"
        elif user.acttype == "lite-v2":
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes')]
            data['limit'] = user.subplans
            data['rlimit'] = user.subplans * 2
            data['dataret'] = 86400
            data['acttype'] = "Lite"
            data['cost'] = "Free"
        elif user.acttype == "enterprise":
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes'),
                ('2mincheck', 'Every 2 Minutes'),
                ('30seccheck', 'Every 30 Seconds')
            ]
            data['limit'] = user.subplans
            data['rlimit'] = user.subplans * 2
            data['cost'] = float(user.subplans) * 6.00
            data['dataret'] = 16070400
            data['acttype'] = "Enterprise"
        else:
            data['choices'] = [
                ('30mincheck', 'Every 30 Minutes'),
                ('5mincheck', 'Every 5 Minutes'),
                ('2mincheck', 'Every 2 Minutes'),
                ('30seccheck', 'Every 30 Seconds')
            ]
            data['limit'] = user.subplans
            data['rlimit'] = user.subplans * 2
            if "yearly" in user.subscription:
                permon = .75 * 12.00
            else:
                permon = 1.00
            data['cost'] = float(user.subplans) * permon
            data['dataret'] = 604800
            data['acttype'] = "Pro"
    data['js_bottom'] = []
    data['js_header'] = []
    data['stripe_pubkey'] = app.config['STRIPE_PUBKEY']
    data['subplans'] = user.subplans
    data['subscription'] = user.subscription
    return data

# Imports (post-app creation)
# ------------------------------------------------------------------


from member.views import member_blueprint
from monitor.views import monitor_blueprint
from public.views import public_blueprint
from reaction.views import reaction_blueprint
from user.views import user_blueprint


# Blueprints
# ------------------------------------------------------------------

app.register_blueprint(member_blueprint)
app.register_blueprint(monitor_blueprint)
app.register_blueprint(public_blueprint)
app.register_blueprint(reaction_blueprint)
app.register_blueprint(user_blueprint)


# Downstream Connections
# ------------------------------------------------------------------

@app.before_request
def before_request():
    '''
    This function establishes a connection
    to the rethinkDB before each connection
    '''
    try:
        g.rdb_conn = r.connect(
            host=app.config['DBHOST'], port=app.config['DBPORT'],
            auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])
    except RqlDriverError:
        # If no connection possible throw 503 error
        abort(503, "No Database Connection Could be Established.")


@app.teardown_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:
        # Who cares?
        pass


# Error handler
# ------------------------------------------------------------------

@app.errorhandler(403)
def forbidden_page(error):
    data = {
        'active': "403",  # Sets the current page
        'loggedin': False  # Don't show the logout link
    }
    return render_template("errors/403.html", data=data), 403


@app.errorhandler(404)
def page_not_found(error):
    # Data is used throughout for the jinja2 templates
    data = {
        'active': "404",  # Sets the current page
        'loggedin': False  # Don't show the logout link
    }
    return render_template("errors/404.html", data=data), 404


@app.errorhandler(500)
def server_error_page(error):
    data = {
        'active': "500",  # Sets the current page
        'loggedin': False  # Don't show the logout link
    }
    return render_template("errors/500.html", data=data), 500


# Initiate the Application
# ------------------------------------------------------------------

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
