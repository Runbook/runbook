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
        data['js_bottom'].append("member/monitors.js")
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
        from generalforms import subscribe

        payment = __import__("payments." + user.payments, globals(),
                             locals(), ['Payments'], -1)

        subscription = payment.Payments(user=user, config=app.config, rdb=g.rdb_conn)
        if request.method == "POST":
            if data['upgraded'] is True:
                result = subscription.adjust(request)
            else:
                result = subscription.create(request)

            if result is True:
                if data['upgraded'] is True:
                    flash('Adjustment to subscription successful', 'success')
                else:
                    data['upgraded'] = True
                    flash('Successfully Subscribed!', 'success')
                newdata = startData(user)
                data['limit'] = newdata['limit']
                data['rlimit'] = newdata['rlimit']
                data['acttype'] = newdata['acttype']
                data['subplans'] = newdata['subplans']
                data['cost'] = newdata['cost']
                data['subscription'] = newdata['subscription']
            else:
                flash('Unable to adjust subscription please notify support', 'danger')
        if data['upgraded'] is True:
            form = subscribe.AddPackForm(request.form)
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
                    result = user.checkPass(form.old_password.data, g.rdb_conn)
                    if result:
                        update = user.setPass(form.password.data, g.rdb_conn)
                        if update:
                            print("/dashboard/user-preferences - Password changed")
                            flash('Password successfully changed.', 'success')
                        else:
                            print("/dashboard/user-preferences - \
                                  Password change failed")
                            flash('Password change was unsuccessful.', 'danger')
                    else:
                        print("/login - User change password error: wrong old password")
                        flash('Old password does not seem valid.', 'danger')
            data['url'] = '/dashboard/user-preferences'
            tmpl = 'member/user-preferences.html'
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        flash('Please Login.', 'warning')
        return redirect(url_for('user.login_page'))
