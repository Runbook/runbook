# public/views.py


import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, abort, Blueprint, render_template

public_blueprint = Blueprint('public', __name__,)

from web import app


@public_blueprint.before_app_request
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


@public_blueprint.teardown_app_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:  # pragma: no cover
        # Who cares?
        pass                # pragma: no cover


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
