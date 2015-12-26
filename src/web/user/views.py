# user/views.py


import time
import stathat
import cookies
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, abort, make_response, Blueprint, request, redirect, \
    url_for, render_template, flash


from users import User
from user.forms import SignupForm, LoginForm
from token import generate_confirmation_token, confirm_token


user_blueprint = Blueprint('user', __name__,)

from web import app, verifyLogin


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
    except RqlDriverError:                      # pragma: no cover
        # If no connection possible throw 503 error
        abort(503, "No Database Connection \
                    Could be Established.")     # pragma: no cover


@user_blueprint.teardown_app_request
def teardown_request(exception):
    ''' This function closes the database connection when done '''
    try:
        g.rdb_conn.close()
    except AttributeError:  # pragma: no cover
        # Who cares?
        pass                # pragma: no cover


###########################
### User View Functions ###
###########################

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
            user.config = app.config
            result = user.createUser(userdata, g.rdb_conn)
            # Check results for success or failure
            if result == "exists":
                flash('User already exists.', 'danger')
            elif result is not False:
                try:
                    stathat.ez_count(
                        app.config['STATHAT_EZ_KEY'],
                        app.config['ENVNAME'] + ' User Signup', 1)
                except:
                    pass
                print("/signup - New user created")
                cdata = cookies.genCdata(result, app.config['SECRET_KEY'])
                data['loggedin'] = True
                flash('You are signed up.', 'success')

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
            flash('Form is not valid.', 'danger')

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
            user.config = app.config
            if user.get('username', email, g.rdb_conn):
                result = user.checkPass(password, g.rdb_conn)
                if result is True:
                    data['loggedin'] = True
                    print("/login - User login successful")
                    flash('You are logged in.', 'success')
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
                    print("/login - User login error: wrong password")
                    flash('Password does not seem valid.', 'danger')
            else:
                print("/login - User login error: invalid user")
                flash('Uhh... User not found.', 'danger')
        else:
            print("/login - User login error: invalid form")
            flash('Form is not valid.', 'danger')

    # Return Login Page
    return render_template('user/login.html', data=data, form=form)


# Logout
@user_blueprint.route('/logout')
def logout_page():
    ''' User logout page: This will unset the cookie '''
    resp = make_response(redirect(url_for('user.login_page')))
    resp.set_cookie('loggedin', 'null', max_age=0)
    print("/logout - User logout")
    return resp


# Confirm Token
@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    verify = verifyLogin(
        app.config['SECRET_KEY'], app.config['COOKIE_TIMEOUT'], request.cookies)
    if verify:
        user = User()
        user.config = app.config
        user.get('uid', verify, g.rdb_conn)
        if user.confirmed:
            flash('Account already confirmed. Thank you.', 'success')
            return redirect(url_for('member.dashboard_page'))
        else:
            try:
                email = confirm_token(token)
                if user.email == email[0]:
                    r.table('users').get(verify).update(
                        {'confirmed': True}).run(g.rdb_conn)
                    flash('You have confirmed your account. Thanks!', 'success')
                    return redirect(url_for('member.dashboard_page'))
                else:
                    flash('The confirmation link is invalid.', 'danger')
                    return redirect(url_for('user.login_page'))
            except:
                flash('The confirmation link is invalid or has expired.',
                      'danger')
                return redirect(url_for('user.login_page'))
    else:
        flash('Please Login.', 'warning')
        return redirect(url_for('user.login_page'))
