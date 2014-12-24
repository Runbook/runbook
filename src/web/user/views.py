# user/views.py


import time
import stathat
import cookies
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, abort, make_response, Blueprint, request, redirect, \
    url_for, render_template


from users import User
from user.forms import SignupForm, LoginForm
from token import generate_confirmation_token


user_blueprint = Blueprint('user', __name__,)

from web import app


@user_blueprint.before_app_request
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


@user_blueprint.teardown_app_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:
        # Who cares?
        pass


# Signup
@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    User Sign up page: Very basic email + password
    sign up form that will also login users.
    '''
    # Data is used throughout for the jinja2 templates
    data = {
        'active': "signup",  # Sets the current page
        'loggedin': False  # Don't show the logout link
    }

    # Define the SignupForm
    form = SignupForm(request.form)
    # Validate and then create userdata
    if request.method == "POST":
        if form.validate():
            # Take form data
            email = form.email.data
            password = form.password.data
            company = form.company.data
            contact = form.contact.data
            userdata = {
                'username': email,
                'email': email,
                'password': password,
                'company': company,
                'contact': contact
            }

            # Create user
            user = User()
            result = user.createUser(userdata, g.rdb_conn)
            # Check results for success or failure
            if result == "exists":
                data['error'] = True
                data['msg'] = 'User already exists'
            elif result is not False:
                stathat.ez_count(
                    app.config['STATHAT_EZ_KEY'],
                    app.config['ENVNAME'] + ' User Signup', 1)
                print("/signup - New user created")
                cdata = cookies.genCdata(result, app.config['SECRET_KEY'])
                data['loggedin'] = True
                data['msg'] = 'You are signed up'
                data['error'] = False

                # Generate confirmation token
                generate_confirmation_token(email, result, time.time())

                # Build response
                resp = make_response(redirect(url_for('member.dashboard_page')))
                timeout = int(time.time()) + int(app.config['COOKIE_TIMEOUT'])
                # Set the cookie secure as best as possible
                resp.set_cookie(
                    'loggedin', cdata, expires=timeout, httponly=True)
                return resp
        else:
            stathat.ez_count(
                app.config['STATHAT_EZ_KEY'],
                app.config['ENVNAME'] + ' False User Signup', 1)
            print("/signup - False user creation")
            data['msg'] = 'Form is not valid'
            data['error'] = True

    # Return Signup Page
    return render_template('user/signup.html', data=data, form=form)


# Login
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    ''' User login page: This is a basic login page'''
    data = {
        'active': 'login',
        'loggedin': False
    }

    # Define and Validate the form
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data

            # Start user definition
            user = User()
            if user.get('username', email, g.rdb_conn):
                result = user.checkPass(password, g.rdb_conn)
                if result is True:
                    data['loggedin'] = True
                    data['msg'] = 'You are logged in'
                    data['error'] = False
                    print("/login - User login successful")
                    # Start building response
                    resp = make_response(
                        redirect(url_for('member.dashboard_page')))
                    cdata = cookies.genCdata(
                        user.uid, app.config['SECRET_KEY'])
                    timeout = int(time.time()) + \
                        int(app.config['COOKIE_TIMEOUT'])
                    # Set cookie as securely as possible
                    resp.set_cookie(
                        'loggedin', cdata, expires=timeout, httponly=True)
                    print("Setting cookie")
                    return resp
                else:
                    data['msg'] = 'Password does not seem valid'
                    data['error'] = True
                    print("/login - User login error: wrong password")
            else:
                data['msg'] = 'Uhh... User not found'
                print("/login - User login error: invalid user")
                data['error'] = True
        else:
            data['msg'] = 'Form is not valid'
            print("/login - User login error: invalid form")
            data['error'] = True

    # Return Login Page
    page = render_template('user/login.html', data=data, form=form)
    return page


# Logout
@user_blueprint.route('/logout')
def logout_page():
    ''' User logout page: This will unset the cookie '''
    resp = make_response(redirect(url_for('user.login_page')))
    resp.set_cookie('loggedin', 'null', max_age=0)
    print("/logout - User logout")
    return resp
