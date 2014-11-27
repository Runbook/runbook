# monitor/views.py


import time
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, Blueprint, render_template, request, \
    url_for, redirect, flash, abort

import stathat
from monitors import Monitor
from users import User

monitor_blueprint = Blueprint('monitor', __name__,)

from web import app, verifyLogin, startData


@monitor_blueprint.before_app_request
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


@monitor_blueprint.teardown_app_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:
        # Who cares?
        pass


# Monitors


# Add a new Monitor
@monitor_blueprint.route('/dashboard/monitors/<cname>', methods=['GET', 'POST'])
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
            tmpl = 'member/mod-subscription.html'
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
@monitor_blueprint.route('/dashboard/edit-monitors/<cname>/<cid>', methods=['GET', 'POST'])
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
            tmpl = 'member/mod-subscription.html'
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
@monitor_blueprint.route('/dashboard/monitors', methods=['GET', 'POST'])
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
            tmpl = 'member/mod-subscription.html'
        else:
            pass
        page = render_template(tmpl, data=data)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Manual Checks
@monitor_blueprint.route('/dashboard/action-checks/<cid>/<action>')
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

    return redirect(url_for('member.dashboard_page'))


# Delete Checks
@monitor_blueprint.route('/dashboard/delete-checks/<cid>')
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
    return redirect(url_for('member.dashboard_page'))


# Web Checks
@monitor_blueprint.route(
    '/api/<atype>/<cid>', methods=['POST'],
    defaults={'check_key': None, 'action': None})
@monitor_blueprint.route(
    '/api/<atype>/<cid>/<check_key>',
    methods=['POST'], defaults={'action': None})
@monitor_blueprint.route('/api/<atype>/<cid>/<check_key>/<action>', methods=['POST'])
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
@monitor_blueprint.route('/dashboard/view-history/<cid>/<start>/<limit>', methods=['GET'])
def viewhistory_page(cid, start, limit):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/view-history/' + cid
        tmpl = 'monitors/view-history.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'member/mod-subscription.html'
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
@monitor_blueprint.route('/dashboard/detail-history/<cid>/<hid>', methods=['GET'])
def detailhistory_page(cid, hid):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/detail-history/' + hid
        tmpl = 'monitors/detail-history.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'member/mod-subscription.html'
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
