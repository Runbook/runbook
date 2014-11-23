import unittest
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from flask import g, abort
from flask.ext.testing import TestCase

from web import app
from users import User
# from user.forms import LoginForm


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        return app

    def setUp(self):
        try:
            g.rdb_conn = r.connect(
                host=app.config['DBHOST'], port=app.config['DBPORT'],
                auth_key=app.config['DBAUTHKEY'], db=app.config['DATABASE'])
        except RqlDriverError:
            # If no connection possible throw 503 error
            abort(503, "No Database Connection Could be Established.")

    def tearDown(self):
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


class TestLoginForm(BaseTestCase):

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        # form = LoginForm(email='ad@min.com', password='admin')
        # self.assertTrue(form.validate())
        pass

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        # form = LoginForm(email='unknown', password='example')
        # self.assertFalse(form.validate())
        pass


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
            # self.assertIn('Dashboard', response.data)
            user = User()
            user = user.get('username', 'test@user.com', g.rdb_conn)
            self.assertTrue(user.email == 'test@user.com')

    # def test_get_by_id(self):
    #     # Ensure id is correct for the current/logged in user
    #     with self.client:
    #         self.client.post('/login', data=dict(
    #             email='ad@min.com', password='admin_user'
    #         ), follow_redirects=True)
    #         self.assertTrue(current_user.id == 1)

    # def test_registered_on_defaults_to_datetime(self):
    #     # Ensure that registered_on is a datetime
    #     with self.client:
    #         self.client.post('/login', data=dict(
    #             email='ad@min.com', password='admin_user'
    #         ), follow_redirects=True)
    #         user = User.query.filter_by(email='ad@min.com').first()
    #         self.assertIsInstance(user.registered_on, datetime.datetime)

    # def test_check_password(self):
    #     # Ensure given password is correct after unhashing
    #     user = User.query.filter_by(email='ad@min.com').first()
    #     self.assertTrue(bcrypt.check_password_hash(user.password, 'admin_user'))
    #     self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

    # def test_validate_invalid_password(self):
    #     # Ensure user can't login when the pasword is incorrect
    #     with self.client:
    #         response = self.client.post('/login', data=dict(
    #             email='ad@min.com', password='foo_bar'
    #         ), follow_redirects=True)
    #     self.assertIn(b'Invalid email and/or password.', response.data)


if __name__ == '__main__':
    unittest.main()
