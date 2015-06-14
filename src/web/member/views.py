# member/views.py


import json
import requests
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, Blueprint, render_template, request, \
    url_for, redirect, abort, flash

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
    except RqlDriverError:                      # pragma: no cover
        # If no connection possible throw 503 error
        abort(503, "No Database Connection \
                    Could be Established.")     # pragma: no cover


@member_blueprint.teardown_app_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:  # pragma: no cover
        # Who cares?
        pass                # pragma: no cover


#############################
### Member View Functions ###
#############################


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
            if len(data['monitors']) < 1:
                data['welcome'] = True
                data['mons'] = False
            else:
                data['welcome'] = False
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
        flash('Please Login.', 'warning')
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

        # Stripe vs ASM stuff
        if user.payments == "ASM":
            headers = {
                "content-type": "application/json",
                "Authorization": app.config['ASSEMBLY_PRIVATE_KEY']
            }
            paymenturl = app.config['ASSEMBLY_PAYMENTS_URL']
        else:
            from base64 import b64encode
            api_key = b64encode(app.config['STRIPE_PRIVATE_KEY']).decode("ascii")
            headers = {
                "Authorization": "Basic " + api_key,
            }
            paymenturl = app.config['STRIPE_PAYMENTS_URL']

        from generalforms import subscribe
        if data['acttype'] != "Pro":
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
                        'source': stripeToken,
                        'plan': plan
                    }
                    json_payload = json.dumps(payload)
                    url = paymenturl + "/customers"
                    print ("Making request to %s") % url
                    try:
                        # Send Request to Payment system to create user and subscribe
                        # them to desired plan
                        result = requests.post(
                            url=url, headers=headers,
                            params=payload, verify=True)
                    except:
                        print("Critical Error making request to Payments")
                        flash('There was an error processing \
                              your card details.', 'danger')
                    print("Got {0} status code from Payments".format(
                        result.status_code))
                    if result.status_code >= 200 and result.status_code <= 299:
                        rdata = json.loads(result.text)
                        user.stripeid = rdata['id']
                        user.stripe = stripeToken
                        user.subplans = payload['quantity']
                        user.subscription = payload['plan']
                        if "pro_plus" in plan:
                            user.acttype = "proplus"
                        else:
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
                            flash('Subscription successfully created.',
                                  'success')
                        else:
                            flash('Subscription not successfully created.',
                                  'danger')
                    else:
                        flash('Subscription not created got status code: %d' % result.status_code, 'danger')
        # Increase subscription
        if data['upgraded']:
            form = subscribe.AddPackForm(request.form)
            if request.method == "POST" and "stripeToken" not in request.form:
                if form.validate():
                    add_packs = int(form.add_packs.data)
                    # Set subscription quantity to desired monitor count
                    payload = {'quantity': add_packs}
                    json_payload = json.dumps(payload)
                    url = paymenturl + "/customers" + user.stripeid
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
                                print("Critical Error making \
                                      request to ASM Payments")
                                flash('An error occured while \
                                      processing the form.', 'danger')
                        else:
                            flash('An error occured while \
                                  processing the form.', 'danger')
                    except:
                        print("Critical Error making request to ASM Payments")
                        flash('An error occured \
                              while processing the form.', 'danger')
                    print("Got {0} status code from Assembly".format(
                        result.status_code))
                    if result.status_code >= 200 and result.status_code <= 299:
                        user.subplans = add_packs
                        # Save user config
                        print("Setting subscription count to \
                              {0} for user {1}".format(add_packs, user.uid))
                        subres = user.setSubscription(g.rdb_conn)
                        if subres:
                            newdata = startData(user)
                            data['limit'] = newdata['limit']
                            data['rlimit'] = newdata['rlimit']
                            data['acttype'] = newdata['acttype']
                            data['subplans'] = newdata['subplans']
                            data['cost'] = newdata['cost']
                            flash('Subscription successfully modified.',
                                  'success')
                        else:
                            flash('Unknown error modifing subscription.',
                                  'danger')

        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        flash('Please Login.', 'warning')
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
                        print("/dashboard/user-preferences - Password changed")
                        flash('Password successfully changed.', 'success')
                    else:
                        print("/dashboard/user-preferences - \
                              Password change failed")
                        flash('Password change was unsuccessful.', 'danger')
            data['url'] = '/dashboard/user-preferences'
            tmpl = 'member/user-preferences.html'
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        flash('Please Login.', 'warning')
        return redirect(url_for('user.login_page'))
