######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests
######################################################################

import unittest
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, abort
from flask.ext.testing import TestCase

from web import app
from users import User
from user.forms import LoginForm, SignupForm


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        return app

    def setUp(self):
        try:
            g.rdb_conn = r.connect(
                host=app.config['DBHOST'], port=app.config['DBPORT'],
                auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])

            userdata = {
                'username': 'test@tester.com',
                'email': 'test@tester.com',
                'password': 'password456',
                'company': 'company',
                'contact': 'tester'
            }

            # Create test user
            user = User()
            user.createUser(userdata, g.rdb_conn)

        except RqlDriverError:
            # If no connection possible throw 503 error
            abort(503, "No Database Connection Could be Established.")

    def tearDown(self):
        # why the need to reconnect?
        g.rdb_conn = r.connect(
            host=app.config['DBHOST'], port=app.config['DBPORT'],
            auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])
        r.db('crdb').table('users').delete().run(g.rdb_conn)
        try:
            g.rdb_conn.close()
        except AttributeError:
            # Who cares?
            pass


class FunctionalTests(BaseTestCase):

    def test_index(self):
        # Ensure that Flask was set up correctly
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('DevOps, automated', response.data)

    def test_dashboard_route_login(self):
        # Ensure that /dashboard requires user login
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn('Login', response.data)

    def test_login_page_loads(self):
        # Ensure that the login page loads correctly
        response = self.client.get('/login')
        self.assertIn('Login', response.data)
        self.assertEqual(response.status_code, 200)

    def test_registration_page_loads(self):
        # Ensure that the registration page loads correctly
        response = self.client.get('/signup')
        self.assertIn('Sign up', response.data)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_route_requires_login(self):
        # Ensure main route requres logged in user.
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn('Login', response.data)

    def test_logout_route_requires_login(self):
        # Ensure logout route requres logged in user.
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn('Login', response.data)

    def test_dashboard_route(self):
        # Ensure registered user can access dashboard route.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertIn('User Preferences', response.data)

    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            user = User()
            user = user.get('username', 'test@tester.com', g.rdb_conn)
            active = user.is_active('test@tester.com', g.rdb_conn)
            self.assertTrue(user.email == "test@tester.com")
            self.assertTrue(active)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly, regarding the session
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn('Login', response.data)

    def test_404_behaves_correctly(self):
        # Ensure 404 error handlers behaves correctly
        response = self.client.get('/not_a_real_page', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn('404', response.data)


class TestLoginForm(BaseTestCase):

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='ad@min.com', password='admin')
        self.assertTrue(form.validate())
        pass

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())
        pass


class TestSignupForm(BaseTestCase):

    def test_validate_success_register_form(self):
        # Ensure correct data validates.
        form = SignupForm(
            email='test@signupform.com',
            company="test",
            contact="test",
            password='signupformtest',
            confirm='signupformtest')
        self.assertTrue(form.validate())

    def test_validate_invalid_password_format(self):
        # Ensure incorrect data does not validate.
        form = SignupForm(
            email='test@signupform.com',
            company="test",
            contact="test",
            password='short',
            confirm='signupformtest')
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register when a duplicate email is used
        form = SignupForm(
            email='test@tester.com',
            company="test",
            contact="test",
            password='short',
            confirm='signupformtest')
        self.assertFalse(form.validate())


class TestUser(BaseTestCase):

    def test_user_registration(self):
        # Ensure user registration behaves correctly.
        with self.client:
            response = self.client.post('/signup', data=dict(
                email='test@user.com',
                company="test",
                contact="test",
                password='test_user',
                confirm='test_user'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Dashboard', response.data)
            user = User()
            user = user.get('username', 'test@user.com', g.rdb_conn)
            self.assertTrue(user.email == 'test@user.com')
            self.assertTrue(user.status == 'active')

    def test_check_password(self):
        # Ensure given password is correct after unhashing
        user = User()
        user = user.get('username', 'test@tester.com', g.rdb_conn)
        self.assertTrue(user.checkPass('password456', g.rdb_conn))
        self.assertFalse(user.checkPass('wrong!', g.rdb_conn))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the pasword is incorrect
        with self.client:
            response = self.client.post('/login', data=dict(
                email='test@tester.com', password='foo_bar'
            ), follow_redirects=True)
        self.assertIn('Password does not seem valid', response.data)


if __name__ == '__main__':
    unittest.main()
