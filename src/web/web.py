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


# Application Configuration
# ------------------------------------------------------------------

app = Flask(__name__)
# Config files are located in the instance directory
configfile = os.path.join('instance', 'web.cfg')
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
        data['choices'] = app.config['PACKAGES'][user.acttype]['choices']
        data['limit'] = user.subplans
        data['rlimit'] = user.subplans * app.config['PACKAGES'][user.acttype]['reaction_multiplier']
        data['dataret'] = app.config['PACKAGES'][user.acttype]['data_retention']
        data['acttype'] = app.config['PACKAGES'][user.acttype]['acttype']
        data['upgraded'] = app.config['PACKAGES'][user.acttype]['upgraded']
        if data['upgraded'] is True:
            if "yearly" in user.subscription:
                data['cost'] = app.config['PACKAGES'][user.acttype]['cost_yearly'] * user.subplans
            else:
                data['cost'] = app.config['PACKAGES'][user.acttype]['cost_monthly'] * user.subplans
        else:
            data['cost'] = 'Free'
        data['stripe_pubkey'] = app.config['STRIPE_PUBKEY']
        data['subplans'] = user.subplans
        data['subscription'] = user.subscription
    data['js_bottom'] = []
    data['js_header'] = []
    return data


# Blueprints
# ------------------------------------------------------------------

from member.views import member_blueprint
from monitor.views import monitor_blueprint
from public.views import public_blueprint
from reaction.views import reaction_blueprint
from user.views import user_blueprint

app.register_blueprint(member_blueprint)
app.register_blueprint(monitor_blueprint)
app.register_blueprint(public_blueprint)
app.register_blueprint(reaction_blueprint)
app.register_blueprint(user_blueprint)


# Error handlers
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
