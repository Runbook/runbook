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
import json
import requests
import sys
import cookies

# Flask modules
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import g
from flask import redirect, url_for

# Gather Stats
import stathat

# Scalable Database
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

# Custom Classes
from forms import ChangePassForm
from users import User
from monitors import Monitor


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


from monitor.views import monitor_blueprint
from public.views import public_blueprint
from reaction.views import reaction_blueprint
from user.views import user_blueprint


# Blueprints
# ------------------------------------------------------------------

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


# Mod-Subscription
@app.route('/dashboard/mod-subscription', methods=['GET', 'POST'])
def modsub_page():
    '''Dashboard Modify Subscription:
    This will allow a user to modify their subscription and account plan
    '''
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/mod-subscription'
        data['uid'] = user.uid
        tmpl = 'monitors/mod-subscription.html'
        data['js_bottom'].append('forms/subscribe.js')
        form = []
        headers = {
            "content-type": "application/json",
            "Authorization": app.config['ASSEMBLY_PRIVATE_KEY']
        }
        from generalforms import subscribe
        if data['acttype'] == "Lite":
            # Upgrade Users
            if request.method == "POST" and \
                    "stripeToken" in request.form and "plan" in request.form:
                stripeToken = request.form['stripeToken']
                plan = request.form['plan']
                if stripeToken:
                    result = None
                    monitor = Monitor()
                    payload = {
                        'email': user.email,
                        'quantity': monitor.count(user.uid, g.rdb_conn),
                        'card': stripeToken,
                        'plan': plan
                    }
                    json_payload = json.dumps(payload)
                    url = app.config['ASSEMBLY_PAYMENTS_URL'] + "/customers"
                    print ("Making request to %s") % url
                    try:
                        # Send Request to Assembly to create user and subscribe
                        # them to desired plan
                        result = requests.post(
                            url=url, headers=headers,
                            data=json_payload, verify=True)
                    except:
                        print("Critical Error making request to ASM Payments")
                        data['msg'] = "There was an error processing your card details"
                        data['error'] = True
                    print(
                        "Got %d status code from Assembly") % result.status_code
                    if result.status_code >= 200 and result.status_code <= 299:
                        rdata = json.loads(result.text)
                        user.stripeid = rdata['id']
                        user.stripe = stripeToken
                        user.subplans = payload['quantity']
                        user.subscription = payload['plan']
                        user.acttype = "pro"
                        print("Setting UID %s Subscription to: %s") % (
                            user.uid, user.acttype)
                        subres = user.setSubscription(g.rdb_conn)
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' User Upgrades', 1)
                        if subres:
                            newdata = startData(user)
                            data['limit'] = newdata['limit']
                            data['rlimit'] = newdata['rlimit']
                            data['acttype'] = newdata['acttype']
                            data['subplans'] = newdata['subplans']
                            data['cost'] = newdata['cost']
                            data['subscription'] = newdata['subscription']
                            data['msg'] = "Subscription successfully created"
                            data['error'] = False
                        else:
                            data[
                                'msg'] = "Subscription not successfully created"
                            data['error'] = True
        # Increase subscription
        if data['acttype'] != "Lite":
            form = subscribe.AddPackForm(request.form)
            if request.method == "POST" and "stripeToken" not in request.form:
                if form.validate():
                    add_packs = int(form.add_packs.data)
                    # Set subscription quantity to desired monitor count
                    payload = {'quantity': add_packs}
                    json_payload = json.dumps(payload)
                    url = app.config[
                        'ASSEMBLY_PAYMENTS_URL'] + "/customers/" + user.stripeid
                    print("Making request to %s") % url
                    try:
                        # Get Subscription ID
                        result = requests.get(
                            url=url, headers=headers, verify=True)
                        if result.status_code == 200:
                            rdata = json.loads(result.text)
                            subsid = rdata['subscriptions']['data'][0]['id']
                            url = url + "/subscriptions/" + subsid
                            print("Making request to %s") % url
                            # Set Quantity
                            try:
                                result = requests.put(
                                    url=url, headers=headers,
                                    data=json_payload, verify=True)
                            except:
                                data['msg'] = "An error occured while processing the form"
                                data['error'] = True
                                print("Critical Error making request to ASM Payments")
                        else:
                            data['msg'] = "An error occured while processing the form"
                            data['error'] = True
                    except:
                        data['msg'] = "An error occured while processing the form"
                        data['error'] = True
                        print("Critical Error making request to ASM Payments")
                    print(
                        "Got %d status code from Assembly") % result.status_code
                    if result.status_code >= 200 and result.status_code <= 299:
                        user.subplans = add_packs
                        # Save user config
                        print("Setting subscription count to %d for user %s") % (add_packs, user.uid)
                        subres = user.setSubscription(g.rdb_conn)
                        if subres:
                            newdata = startData(user)
                            data['limit'] = newdata['limit']
                            data['rlimit'] = newdata['rlimit']
                            data['acttype'] = newdata['acttype']
                            data['subplans'] = newdata['subplans']
                            data['cost'] = newdata['cost']
                            data['msg'] = "Subscription successfully modified"
                            data['error'] = False
                        else:
                            data['msg'] = "Unknown error modifing subscription"
                            data['error'] = True

        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


# User-Preferences
@app.route('/dashboard/user-preferences', methods=['GET', 'POST'])
def userpref_page():
    '''
    Dashbaord User Preferences:
    This will allow a user to change user preferences, i.e. Password
    '''
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'monitors/mod-subscription.html'
        else:

            # Start processing the change password form
            form = ChangePassForm(request.form)
            if request.method == 'POST':
                if form.validate():
                    result = user.setPass(form.password.data, g.rdb_conn)
                    if result:
                        data['msg'] = "Password successfully changed"
                        print("/dashboard/user-preferences - Password changed")
                        data['error'] = False
                    else:
                        data['msg'] = "Password change was unsuccessful"
                        print("/dashboard/user-preferences - Password change failed")
                        data['error'] = True
            data['url'] = '/dashboard/user-preferences'
            tmpl = 'user-preferences.html'
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


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
