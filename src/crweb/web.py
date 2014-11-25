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
import time
import requests
import sys
import cookies

# Flask modules
from flask import Flask
from flask import render_template
from flask import request
from flask import abort, flash
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
from reactions import Reaction


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

from public.views import public_blueprint
from user.views import user_blueprint


# Blueprints
# ------------------------------------------------------------------

app.register_blueprint(public_blueprint)
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


# Dashboard


# Dashboard Home
@app.route('/dashboard')
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
        data['js_bottom'].append("screen-o-death.js")
        data['js_bottom'].append("screen-o-death-chart.js")
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            page = render_template('mod-subscription.html', data=data)
        else:

            data['monitors'] = user.getMonitors(g.rdb_conn)
            data['reactions'] = user.getReactions(g.rdb_conn)
            data['monevents'] = user.getEvents(g.rdb_conn)
            data['moneventsnum'] = len(data['monevents'])
            data['monstats'] = {'healthy': 0,
                                'unknown': 0,
                                'failed': 0}
            for key in data['monitors'].keys():
                if "healthy" in data['monitors'][key]['status']:
                    data['monstats']['healthy'] = data[
                        'monstats']['healthy'] + 1
                elif "failed" in data['monitors'][key]['status']:
                    data['monstats']['failed'] = data['monstats']['failed'] + 1
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
            page = render_template('screen-o-death.html', data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Monitors


# Add a new Monitor
@app.route('/dashboard/monitors/<cname>', methods=['GET', 'POST'])
def addcheck_page(cname):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/monitors/' + cname
        tmpl = 'monitors/' + cname + '.html'
        data['js_bottom'] = ['monitors/base.js', 'monitors/' + cname + '.js']
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:
            # Get list of reactions and validate that there are some
            data['reactions'] = user.getReactions(g.rdb_conn)
            # Proces the form
            cform = __import__(
                "monitorforms." + cname, globals(), locals(), ['CheckForm'], -1)
            form = cform.CheckForm(request.form)
            if form.__contains__("timer"):
                form.timer.choices = data['choices']
            reactchoices = []
            for key in data['reactions'].keys():
                reactchoices.append(
                    (data['reactions'][key]['id'],
                        data['reactions'][key]['name']))
            form.reactions.choices = reactchoices
            if request.method == 'POST':
                if form.validate():
                    monitor = Monitor()
                    monitor.name = form.name.data
                    monitor.ctype = cname
                    monitor.uid = user.uid
                    monitor.status = "queued"
                    monitor.url = None
                    tmpdata = {}
                    for item in form.__iter__():
                        tmpdata[item.name] = item.data
                    monitor.data = tmpdata

                    # Check if the user already exceeds their limit
                    if monitor.count(user.uid, g.rdb_conn) < data['limit']:
                        # Create the monitor if all checks out
                        results = monitor.createMonitor(g.rdb_conn)
                    else:
                        results = "toomany"

                    if results == "exists":
                        data['msg'] = "This monitor seems to already exist, try using a different name: %s" % monitor.name
                        print("/dashboard/monitors/%s - Monitor already exists") % cname
                        data['error'] = True
                    elif results is False:
                        data['msg'] = "Could not create monitor"
                        print("/dashboard/monitors/%s - Monitor creation failed") % cname
                        data['error'] = True
                    elif results == 'toomany':
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' Too many health checks',
                            1)
                        data['msg'] = "You have too many monitors [%d] to add another. Please upgrade your plan or clean up old ones." % data['limit']
                        print("/dashboard/monitors/%s - Monitor creation failed: toomany") % cname
                        data['error'] = True
                    else:
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' Monitor Added', 1)
                        data['msg'] = 'Monitor "%s" successfully added' % monitor.name
                        print("/dashboard/monitors/%s - Monitor creation successful") % cname
                        data['error'] = False
                        newmonitor = Monitor()
                        newmonitor.get(results, g.rdb_conn)
                        if newmonitor.uid == user.uid:
                            data['monitor'] = {
                                'cid': newmonitor.cid,
                                'name': newmonitor.name,
                                'uid': newmonitor.uid,
                                'ctype': newmonitor.ctype,
                                'url': newmonitor.url,
                                'data': newmonitor.data
                            }
                else:
                    print("/dashboard/monitors/%s - Monitor creation failed: Form invalid") % cname
                    data['msg'] = "Form is not valid"
                    data['error'] = True
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Edit a Monitor
@app.route('/dashboard/edit-monitors/<cname>/<cid>', methods=['GET', 'POST'])
def editcheck_page(cname, cid):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/edit-monitors/' + cname + "/" + cid
        tmpl = 'monitors/' + cname + '.html'
        data['edit'] = True
        data['js_bottom'] = ['monitors/base.js', 'monitors/' + cname + '.js']
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:
            # Get list of reactions and validate that there are some
            data['reactions'] = user.getReactions(g.rdb_conn)
            # Proces the form
            cform = __import__(
                "monitorforms." + cname, globals(), locals(), ['CheckForm'], -1)
            form = cform.CheckForm(request.form)
            oldmonitor = Monitor()
            oldmonitor.get(cid, g.rdb_conn)
            if oldmonitor.uid == user.uid:
                data['monitor'] = {
                    'cid': oldmonitor.cid,
                    'name': oldmonitor.name,
                    'uid': oldmonitor.uid,
                    'ctype': oldmonitor.ctype,
                    'url': oldmonitor.url,
                    'data': oldmonitor.data
                }
            # Check if the form contains the timer SelectField
            if form.__contains__("timer"):
                form.timer.choices = data['choices']
            reactchoices = []
            reactdefaults = []
            for key in data['reactions'].keys():
                reactchoices.append(
                    (data['reactions'][key]['id'],
                        data['reactions'][key]['name']))
                if data['reactions'][key]['id'] in \
                        data['monitor']['data']['reactions']:
                    reactdefaults.append(data['reactions'][key]['id'])
            form.reactions.choices = reactchoices
            for item in form.__iter__():
                if item.type == "SelectField" or\
                        item.type == "SelectMultipleField":
                    item.default = data['monitor']['data'][item.name]

            if request.method == 'POST':
                if form.validate():
                    monitor = Monitor()
                    monitor.cid = cid
                    monitor.name = form.name.data
                    monitor.ctype = cname
                    monitor.uid = user.uid
                    monitor.status = "queued"
                    monitor.url = oldmonitor.url
                    tmpdata = {}
                    for item in form.__iter__():
                        tmpdata[item.name] = item.data
                        if item.type == "SelectField" or\
                                item.type == "SelectMultipleField":
                            item.default = item.data
                    monitor.data = tmpdata
                    data['monitor'] = {
                        'cid': monitor.cid,
                        'name': monitor.name,
                        'uid': monitor.uid,
                        'ctype': monitor.ctype,
                        'url': monitor.url,
                        'data': monitor.data
                    }
                    reactdefaults = data['monitor']['data']['reactions']
                    # Check if the user already exceeds their limit
                    if oldmonitor.uid == user.uid:
                        # Create the monitor if all checks out
                        results = monitor.editMonitor(g.rdb_conn)
                    else:
                        results = "NotYours"
                        data['msg'] = "This Monitor doesn't appear to be yours"
                        print("/dashboard/edit-monitors/%s - Monitor edit failed: not users") % cname
                        data['error'] = True
                    if results == "exists":
                        data['msg'] = "This monitor seems to already exist, try using a different name: %s" % monitor.name
                        print("/dashboard/edit-monitors/%s - Monitor edit failed: exists") % cname
                        data['error'] = True
                    elif results is False:
                        data['msg'] = "Could not edit monitor"
                        print("/dashboard/edit-monitors/%s - Monitor edit failed: unknown reason") % cname
                        data['error'] = True
                    elif results == 'toomany':
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' Too many health checks',
                            1)
                        data['msg'] = "You have too many monitors [%d] to add another. Please upgrade your plan or clean up old ones." % data['limit']
                        print("/dashboard/edit-monitors/%s - Monitor edit failed: too many") % cname
                        data['error'] = True
                    else:
                        stathat.ez_count(app.config['STATHAT_EZ_KEY'], app.config['ENVNAME'] + ' Monitor Added', 1)
                        data['msg'] = 'Monitor "%s" successfully edited' % monitor.name
                        print("/dashboard/edit-monitors/%s - Monitor edit successful") % cname
                        data['error'] = False
                else:
                    data['msg'] = "Form is not valid"
                    print("/dashboard/edit-monitors/%s - Monitor edit failed: Form invalid") % cname
                    data['error'] = True
            # Process form to display defaults
            if form.__contains__("timer"):
                form.timer.default = data['monitor']['data']['timer']
            form.reactions.default = reactdefaults
            form.process()
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Monitors Index
@app.route('/dashboard/monitors', methods=['GET', 'POST'])
def monitors_page():
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/monitors/'
        tmpl = 'monitors/index.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:
            pass
        page = render_template(tmpl, data=data)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Manual Checks
@app.route('/dashboard/action-checks/<cid>/<action>')
def checkaction_page(cid, action):
    '''
    Dashboard Delete Checks:
    This will delete health checks via the url parameters
    '''
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        if user.status != "active":
            pass
        else:

            # Delete the Monitor
            monitor = Monitor(cid)
            monitor.get(cid, g.rdb_conn)
            if user.uid == monitor.uid:
                if action == "failed":
                    monitor.healthcheck = "web-failed"
                    result = monitor.webCheck(g.rdb_conn)
                    print("/dashboard/action-checks - Manual monitor failure")
                elif action == "healthy":
                    monitor.healthcheck = "web-healthy"
                    print("/dashboard/action-checks - Manual monitor healthy")
                    result = monitor.webCheck(g.rdb_conn)

                if result:
                    print("/dashboard/action-checks - Manual monitor queued")
                    flash('Health check status change is queued', 'success')
                else:
                    print("/dashboard/action-checks - Manual monitor action failed")
                    flash(
                        'Something went wrong. Could not modify health check',
                        'danger')
            else:
                print("/dashboard/action-checks - Manual monitor action failed: do not own")
                flash('It does not appear you own this health check', 'danger')

    return redirect(url_for('dashboard_page'))


# Delete Checks
@app.route('/dashboard/delete-checks/<cid>')
def delcheck_page(cid):
    '''
    Dashboard Delete Checks:
    This will delete health checks via the url parameters
    '''
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        if user.status != "active":
            pass
        else:

            # Delete the Monitor
            monitor = Monitor(cid)
            monitor.get(cid, g.rdb_conn)
            result = monitor.deleteMonitor(user.uid, cid, g.rdb_conn)
            if result:
                print("/dashboard/delete-checks - Delete successful")
                flash('Health Check was successfully deleted', 'success')
            else:
                print("/dashboard/delete-checks - Delete failed")
                flash('Health Check was not deleted', 'danger')
    return redirect(url_for('dashboard_page'))


# Web Checks
@app.route(
    '/api/<atype>/<cid>', methods=['POST'],
    defaults={'check_key': None, 'action': None})
@app.route(
    '/api/<atype>/<cid>/<check_key>',
    methods=['POST'], defaults={'action': None})
@app.route('/api/<atype>/<cid>/<check_key>/<action>', methods=['POST'])
def checkapi_page(atype, cid, check_key, action):
    ''' Web based API for various health checks '''
    monitor = Monitor(cid)
    urldata = {
        'cid': cid,
        'atype': atype,
        'check_key': check_key,
        'action': action
    }
    try:
        webapi = __import__(
            "monitorapis." + atype, globals(), locals(), ['webCheck'], -1)
        replydata = webapi.webCheck(request, monitor, urldata, g.rdb_conn)
    except:
        print("/api/%s - webCheck action") % atype
        replydata = {
            'headers': {'Content-type': 'application/json'},
            'data': "{ 'results' : 'fatal error' }"
        }

    print("/api/%s - API request") % atype
    return replydata['data']


## History and Tracking

# View Monitor History
@app.route('/dashboard/view-history/<cid>/<start>/<limit>', methods=['GET'])
def viewhistory_page(cid, start, limit):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/view-history/' + cid
        tmpl = 'view-history.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:
            monitor = Monitor()
            monitor.get(cid, g.rdb_conn)
            if monitor.uid == user.uid:
                data['monitor'] = {
                    'cid': monitor.cid,
                    'name': monitor.name,
                    'ctype': monitor.ctype,
                    'uid': monitor.uid,
                    'data': monitor.data
                }
                chktime = time.time() - float(data['dataret'])
                data['monitor-history-count'] = monitor.history(
                    method="count", time=chktime, rdb=g.rdb_conn)
                data['monitor-history'] = monitor.history(
                    method="mon-history", time=chktime,
                    start=int(start), limit=int(limit), rdb=g.rdb_conn)
                data['error'] = False
                data['monitor-history-paging'] = []
                data['monitor-history-paging-start'] = int(start)
                cur = 0
                while cur < data['monitor-history-count'] - 200:
                    cur = cur + 200
                    data['monitor-history-paging'].append(cur)
            else:
                data['msg'] = "This monitor does not belong to your user"
                data['error'] = True
        page = render_template(tmpl, data=data)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Detail Monitor History
@app.route('/dashboard/detail-history/<cid>/<hid>', methods=['GET'])
def detailhistory_page(cid, hid):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/detail-history/' + hid
        tmpl = 'detail-history.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:
            monitor = Monitor()
            monitor.get(cid, g.rdb_conn)
            if monitor.uid == user.uid:
                data['monitor'] = {
                    'cid': monitor.cid,
                    'name': monitor.name,
                    'ctype': monitor.ctype,
                    'uid': monitor.uid,
                    'data': monitor.data
                }
                data['monitor-history'] = monitor.history(
                    method="detail-history", hid=hid, rdb=g.rdb_conn)
                data['error'] = False
            else:
                data['msg'] = "This monitor does not belong to your user"
                data['error'] = True
        page = render_template(tmpl, data=data)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Reactions

# Add a new reaction
@app.route('/dashboard/reactions/<rname>', methods=['GET', 'POST'])
def addreaction_page(rname):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/reactions/' + rname
        tmpl = 'reactions/' + rname + '.html'
        data['js_bottom'] = ['reactions/base.js', 'reactions/' + rname + '.js']
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:

            reform = __import__(
                "reactionforms." + rname, globals(),
                locals(), ['ReactForm'], -1)
            form = reform.ReactForm(request.form)
            if request.method == 'POST':
                if form.validate():
                    reaction = Reaction()
                    reaction.name = form.name.data
                    reaction.trigger = form.trigger.data
                    reaction.frequency = form.frequency.data
                    reaction.uid = user.uid
                    reaction.rtype = rname
                    tmpdata = {}
                    for item in form.__iter__():
                        tmpdata[item.name] = item.data
                    reaction.data = tmpdata

                    if reaction.count(user.uid, g.rdb_conn) < data['rlimit']:
                        results = reaction.createReaction(g.rdb_conn)
                    else:
                        results = "toomany"

                    if results == "exists":
                        data['msg'] = "This reaction seems to already exist, try using a different name: %s" % reaction.name
                        print("/dashboard/reactions/%s - Reaction creation failed: exists") % rname
                        data['error'] = True
                    elif results == "edit noexists":
                        data['msg'] = "This reaction can not be edited as it does not exist: %s" % reaction.name
                        print("/dashboard/reactions/%s - Reaction edit failed: doesnt exist") % rname
                        data['error'] = True
                    elif results == "edit true":
                        data['msg'] = "Reaction successfully edited: %s" % reaction.name
                        print("/dashboard/reactions/%s - Reaction edit successful") % rname
                        data['error'] = False
                    elif results == "edit false":
                        data['msg'] = "Reaction not successfully edited: %s" % reaction.name
                        print("/dashboard/reactions/%s - Reaction edit failed: unknown") % rname
                        data['error'] = True
                    elif results == "toomany":
                        data['msg'] = "Could not create reaction: Too many reactions already created [%d]" % data[
                            'rlimit']
                        print(
                            "/dashboard/reactions/%s - Reaction creation failed: too many") % rname
                        data['error'] = True
                    elif results is False:
                        data['msg'] = "Could not create reaction"
                        print("/dashboard/reactions/%s - Reaction creation failed: unknown") % rname
                        data['error'] = True
                    else:
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' Reaction Added', 1)
                        data['msg'] = 'Reaction "%s" successfully added' % reaction.name
                        print("/dashboard/reactions/%s - Reaction creation successful") % rname
                        data['error'] = False
                else:
                    data['msg'] = "Form is not valid"
                    print("/dashboard/reactions/%s - Reaction creation failed: form invalid") % rname
                    data['error'] = True

        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Edit an existing reaction
@app.route('/dashboard/edit-reactions/<rname>/<rid>', methods=['GET', 'POST'])
def editreact_page(rname, rid):
    ''' This is a generic edit page for reactions '''
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/edit-reactions/' + rname + '/' + rid
        tmpl = 'reactions/index.html'
        data['js_bottom'] = ['reactions/base.js', 'reactions/' + rname + '.js']
        data['edit'] = True
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:
            reform = __import__(
                "reactionforms." + rname, globals(),
                locals(), ['ReactForm'], -1)
            form = reform.ReactForm(request.form)
            reaction = Reaction()
            # If Edit get information
            reaction.get("rid", rid, g.rdb_conn)
            if reaction.uid == user.uid:
                data['reaction'] = {
                    'rid': reaction.rid,
                    'name': reaction.name,
                    'trigger': reaction.trigger,
                    'frequency': reaction.frequency,
                    'uid': reaction.uid,
                    'rtype': reaction.rtype,
                    'data': reaction.data
                }
            data['selects'] = []
            for item in form.__iter__():
                if item.type == "SelectField" or \
                        item.type == "SelectMultipleField":
                    item.default = data['reaction']['data'][item.name]
            tmpl = 'reactions/' + rname + '.html'
            if request.method == 'POST':
                if form.validate():
                    reaction2 = Reaction()
                    reaction2.rid = reaction.rid
                    reaction2.name = form.name.data
                    reaction2.trigger = form.trigger.data
                    reaction2.frequency = form.frequency.data
                    reaction2.lastrun = reaction.lastrun
                    reaction2.uid = user.uid
                    reaction2.rtype = reaction.rtype
                    tmpdata = {}
                    for item in form.__iter__():
                        tmpdata[item.name] = item.data
                        if item.type == "SelectField" or\
                                item.type == "SelectMultipleField":
                            item.default = item.data
                    reaction2.data = tmpdata

                    data['reaction'] = {
                        'rid': reaction2.rid,
                        'name': reaction2.name,
                        'trigger': reaction2.trigger,
                        'frequency': reaction2.frequency,
                        'uid': reaction2.uid,
                        'rtype': reaction2.rtype,
                        'data': reaction2.data
                    }
                    if reaction.uid == user.uid:
                        results = reaction2.editReaction(g.rdb_conn)
                    else:
                        results = False
                        data['msg'] = "It doesn't appear that you own this reaction"
                        print("/dashboard/reactions/%s - Reaction edit failed: not owner") % rname
                        data['error'] = True
                    if results == "exists":
                        data['msg'] = "This reaction seems to already exist, try using a different name: %s" % reaction2.name
                        print("/dashboard/reactions/%s - Reaction edit failed: exists") % rname
                        data['error'] = True
                    elif results == "edit noexists":
                        data['msg'] = "This reaction can not be edited as it does not exist: %s" % reaction2.name
                        print("/dashboard/reactions/%s - Reaction edit failed: exists") % rname
                        data['error'] = True
                    elif results == "edit true":
                        data['msg'] = "Reaction successfully edited: %s" % reaction2.name
                        print("/dashboard/reactions/%s - Reaction edit successful") % rname
                        data['error'] = False
                    elif results == "edit false":
                        data['msg'] = "Reaction not successfully edited: %s" % reaction2.name
                        print("/dashboard/reactions/%s - Reaction edit failed: unknown") % rname
                        data['error'] = True
                    elif results is False:
                        data['msg'] = "Could not create reaction"
                        print("/dashboard/reactions/%s - Reaction edit failed: unknown") % rname
                        data['error'] = True
                    else:
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' Reaction Added', 1)
                        data['msg'] = 'Reaction "%s" successfully added' % reaction2.name
                        print("/dashboard/reactions/%s - Reaction edit success") % rname
                        data['error'] = False
                else:
                    data['msg'] = "Form is not valid"
                    print("/dashboard/reactions/%s - Reaction edit failed: form invalid") % rname
                    data['error'] = True
        form.process()
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Reaction Index
@app.route('/dashboard/reactions', methods=['GET', 'POST'])
def reactions_page():
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/reactions/'
        tmpl = 'reactions/index.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'mod-subscription.html'
        else:
            pass
        page = render_template(tmpl, data=data)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Delete Reaction
@app.route('/dashboard/delete-reaction/<rid>')
def delreaction_page(rid):
    '''
    Dashboard Delete Domains:
    This will delete a domain based on url parameters
    '''
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        if user.status != "active":
            pass
        else:

            appliedcount = 0
            results = r.table('monitors').filter(
                {'uid': user.uid}).run(g.rdb_conn)
            for x in results:
                if rid in x['data']['reactions']:
                    appliedcount = appliedcount + 1

            if appliedcount < 1:
                # Delete the Reaction
                reaction = Reaction(rid)
                result = reaction.deleteReaction(user.uid, rid, g.rdb_conn)
                if result:
                    flash('Reaction was successfully deleted', 'success')
                else:
                    flash('Reaction was not deleted', 'danger')
            else:
                flash('You must first detach this reaction from all monitors before deleting', 'danger')
    return redirect(url_for('dashboard_page'))


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
        tmpl = 'mod-subscription.html'
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
            tmpl = 'mod-subscription.html'
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
