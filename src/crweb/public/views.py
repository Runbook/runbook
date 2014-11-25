# public/views.py


import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, abort, Blueprint, render_template, request, \
    url_for, redirect

from users import User

public_blueprint = Blueprint('public', __name__,)

from web import app, verifyLogin, startData


@public_blueprint.before_request
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


@public_blueprint.teardown_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:
        # Who cares?
        pass


# Index
@public_blueprint.route('/')
def index_redirect():
    ''' User login page: This is a basic login page'''
    data = {
        'active': '/',
        'clean_header': True,
        'loggedin': False
    }

    # Return Home Page
    return render_template('public/index.html', data=data)


# Static Pages
@public_blueprint.route("/pages/<pagename>", methods=['GET'])
def static_pages(pagename):
    ''' Generate static pages if they are defined '''
    rendpage = '404.html'
    status_code = 404
    for page in app.config['STATIC_PAGES'].keys():
        # This is less efficent but it lessens the chance
        # of users rendering templates they shouldn't
        if pagename == page:
            rendpage = app.config['STATIC_PAGES'][page]
            status_code = 200

    data = {
        'active': pagename,
        'loggedin': False
    }
    return render_template('public/'+rendpage, data=data), status_code


# Dashboard Home
@public_blueprint.route('/dashboard')
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
        data['js_bottom'].append("public/screen-o-death.js")
        data['js_bottom'].append("public/screen-o-death-chart.js")
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
            page = render_template(
                'public/screen-o-death.html', data=data, form=form)
        return page
    else:
        return redirect(url_for('user.login_page'))
