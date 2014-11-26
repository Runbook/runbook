# monitor/views.py


import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, Blueprint, render_template, request, \
    url_for, redirect, flash, abort

import stathat
from reactions import Reaction
from users import User

reaction_blueprint = Blueprint('reaction', __name__,)

from web import app, verifyLogin, startData


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

# Reactions

# Add a new reaction
@reaction_blueprint.route('/dashboard/reactions/<rname>', methods=['GET', 'POST'])
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
            tmpl = 'monitors/mod-subscription.html'
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
                        data['msg'] = "Could not create reaction: Too many reactions already created [%d]" % data['rlimit']
                        print("/dashboard/reactions/%s - Reaction creation failed: too many") % rname
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
@reaction_blueprint.route('/dashboard/edit-reactions/<rname>/<rid>', methods=['GET', 'POST'])
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
            tmpl = 'monitors/mod-subscription.html'
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
@reaction_blueprint.route('/dashboard/reactions', methods=['GET', 'POST'])
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
            tmpl = 'monitors/mod-subscription.html'
        else:
            pass
        page = render_template(tmpl, data=data)
        return page
    else:
        return redirect(url_for('user.login_page'))


# Delete Reaction
@reaction_blueprint.route('/dashboard/delete-reaction/<rid>')
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
    return redirect(url_for('public.dashboard_page'))
