# member/views.py


import json
import requests
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, Blueprint, render_template, request, \
    url_for, redirect, abort

import stathat
from monitors import Monitor
from users import User
from forms import ChangePassForm

member_blueprint = Blueprint('member', __name__,)

from web import app, verifyLogin, startData


@member_blueprint.before_app_request
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


@member_blueprint.teardown_app_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:
        # Who cares?
        pass


# Dashboard Home
@member_blueprint.route('/dashboard')
def dashboard_page():
    ''' Dashboard: Generate the Welcome/Status page for the dashboard '''
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard'
        data['js_bottom'].append("member/screen-o-death.js")
        data['js_bottom'].append("member/screen-o-death-chart.js")
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            page = render_template('member/mod-subscription.html', data=data)
        else:

            data['monitors'] = user.getMonitors(g.rdb_conn)
            data['reactions'] = user.getReactions(g.rdb_conn)
            data['monevents'] = user.getEvents(g.rdb_conn)
            data['moneventsnum'] = len(data['monevents'])
            data['monstats'] = {'true': 0,
                                'unknown': 0,
                                'false': 0}
            for key in data['monitors'].keys():
                if "true" in data['monitors'][key]['status']:
                    data['monstats']['true'] = data[
                        'monstats']['true'] + 1
                elif "false" in data['monitors'][key]['status']:
                    data['monstats']['false'] = data['monstats']['false'] + 1
                else:
                    data['monstats']['unknown'] = data[
                        'monstats']['unknown'] + 1

            # If there are no monitors print a welcome message
            if len(data['monitors']) < 1 and len(data['reactions']) < 1:
                data['welcome'] = True
            else:
                data['welcome'] = False

            if len(data['monitors']) < 1:
                data['mons'] = False
            else:
                data['mons'] = True

            if len(data['reactions']) < 1:
                data['reacts'] = False
            else:
                data['reacts'] = True

            from generalforms import subscribe
            form = subscribe.AddPackForm(request.form)
            page = render_template(
                'member/screen-o-death.html', data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Mod-Subscription
@member_blueprint.route('/dashboard/mod-subscription', methods=['GET', 'POST'])
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
        tmpl = 'member/mod-subscription.html'
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
@member_blueprint.route('/dashboard/user-preferences', methods=['GET', 'POST'])
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
            tmpl = 'member/mod-subscription.html'
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
            tmpl = 'member/user-preferences.html'
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))
