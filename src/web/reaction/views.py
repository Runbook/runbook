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


@reaction_blueprint.before_app_request
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


@reaction_blueprint.teardown_app_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:  # pragma: no cover
        # Who cares?
        pass                # pragma: no cover


###############################
### Reaction View Functions ###
###############################


# Add a new reaction
@reaction_blueprint.route(
    '/dashboard/reactions/<rname>', methods=['GET', 'POST'])
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
            tmpl = 'member/mod-subscription.html'
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
                        print("/dashboard/reactions/{0} - \
                            Reaction creation failed: exists".format(rname))
                        flash('{0} seems to already exist. Try using a \
                              different name.'.format(reaction.name), 'danger')
                    elif results == "edit noexists":
                        print("/dashboard/reactions/{0} - Reaction \
                              edit failed: doesn't exist".format(rname))
                        flash('{0} cannot be edited as it does not \
                              exist.'.format(reaction.name), 'danger')
                    elif results == "edit true":
                        print("/dashboard/reactions/{0} - \
                              Reaction edit successful".format(rname))
                        flash('Reaction successfully edited: {0}.'.format(
                            reaction.name), 'success')
                    elif results == "edit failed":
                        print("/dashboard/reactions/{0} - \
                              Reaction edit failed: unknown".format(rname))
                        flash('Reaction not successfully edited: {0}.'.format(
                            reaction.name), 'danger')
                    elif results == "toomany":
                        print("/dashboard/reactions/{0} - \
                              Reaction creation failed: too many".format(rname))
                        flash('Could not create reaction: \
                              Too many reactions already created.', 'danger')
                    elif results is False:
                        print("/dashboard/reactions/{0} - \
                              Reaction creation failed: unknown".format(rname))
                        flash('Could not create reaction.', 'danger')
                    else:
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' Reaction Added', 1)
                        print("/dashboard/reactions/{0} - \
                              Reaction creation successful".format(rname))
                        flash('Reaction "{0}" successfully added.'.format(
                            reaction.name), 'success')
                else:
                    print("/dashboard/reactions/{0} - \
                          Reaction creation failed: form invalid".format(rname))
                    flash('Form is not valid.', 'success')

        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        flash('Please Login.', 'warning')
        return redirect(url_for('user.login_page'))


# Edit an existing reaction
@reaction_blueprint.route(
    '/dashboard/edit-reactions/<rname>/<rid>', methods=['GET', 'POST'])
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
            tmpl = 'member/mod-subscription.html'
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
                        print("/dashboard/reactions/{0} - \
                            Reaction edit failed: not owner".format(rname))
                        flash("It doesn't appear that you own this reaction.",
                              'danger')
                    if results == "exists":
                        print("/dashboard/reactions/{0} - \
                              Reaction edit failed: exists".format(rname))
                        flash('This reaction seems to already exist. \
                              Try using a different name.', 'danger')
                    elif results == "edit noexists":
                        print("/dashboard/reactions/{0} - \
                              Reaction edit failed: exists".format(rname))
                        flash('This reaction can not be edited \
                              as it does not exist.', 'danger')
                    elif results == "edit true":
                        print("/dashboard/reactions/{0} - \
                              Reaction edit successful".format(rname))
                        flash('Reaction successfully edited.', 'success')
                    elif results == "edit failed":
                        print("/dashboard/reactions/{0} - \
                              Reaction edit failed: unknown".format(rname))
                        flash('Reaction not successfully edited.', 'danger')
                    elif results is False:
                        print("/dashboard/reactions/{0} - \
                              Reaction edit failed: unknown".format(rname))
                        flash('Could not create reaction.', 'danger')
                    else:
                        stathat.ez_count(
                            app.config['STATHAT_EZ_KEY'],
                            app.config['ENVNAME'] + ' Reaction Added', 1)
                        print("/dashboard/reactions/{0} - \
                              Reaction edit success".format(rname))
                        flash('Reaction "{0}" successfully \
                              added.'.format(reaction2.name), 'danger')
                else:
                    print("/dashboard/reactions/{0} - \
                          Reaction edit failed: form invalid".format(rname))
                    flash('Form is not valid.', 'danger')
        form.process()
        page = render_template(tmpl, data=data, form=form)
        return page
    else:
        flash('Please Login.', 'warning')
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
        data['reaction_list'] = app.config['REACTIONS']
        data['js_bottom'] = [ 'reactions/reactionlist.js' ]
        tmpl = 'reactions/index.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'member/mod-subscription.html'
        else:
            pass
        data['reactions'] = user.getReactions(g.rdb_conn)
        if len(data['reactions']) < 1:
            data['reacts'] = False
        else:
            data['reacts'] = True
        page = render_template(tmpl, data=data)
        return page
    else:
        flash('Please Login.', 'warning')
        return redirect(url_for('user.login_page'))


# Reaction Index
@reaction_blueprint.route('/dashboard/manage-reactions', methods=['GET', 'POST'])
def managereactions_page():
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.get('uid', verify, g.rdb_conn)
        data = startData(user)
        data['active'] = 'dashboard'
        data['url'] = '/dashboard/reactions/'
        data['js_bottom'] = [ 'member/reactions.js' ]
        tmpl = 'member/reactions.html'
        # Check Users Status
        if user.status != "active":
            data['url'] = '/dashboard/mod-subscription'
            tmpl = 'member/mod-subscription.html'
        else:
            pass
        data['reactions'] = user.getReactions(g.rdb_conn)
        if len(data['reactions']) < 1:
            data['reacts'] = False
        else:
            data['reacts'] = True
        page = render_template(tmpl, data=data)
        return page
    else:
        flash('Please Login.', 'warning')
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
                    flash('Reaction was successfully deleted.', 'success')
                else:
                    flash('Reaction was not deleted.', 'danger')
            else:
                flash('You must first detach this reaction \
                      from all monitors before deleting.', 'danger')
    return redirect(url_for('member.dashboard_page'))
