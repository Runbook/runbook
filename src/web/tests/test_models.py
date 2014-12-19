######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - models
######################################################################


import unittest

from flask import g, request

from base import BaseTestCase
from users import User
from web import app, verifyLogin


class TestUserModel(BaseTestCase):

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
            self.assertTrue(user.is_active('test@tester.com', g.rdb_conn))

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

    def test_check_if_confirmed_before_confirming(self):
        # Ensure an "unconfimered" user is not "confirmed"
        user = User()
        user = user.get('username', 'test@tester.com', g.rdb_conn)
        self.assertFalse(user.is_confirmed('username', g.rdb_conn))

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in user
        with self.client:
            response = self.client.post('/login', data=dict(
                email='test@tester.com', password='password456'
            ), follow_redirects=True)
            print response
            logged_in_user_id = verifyLogin(
                app.config['SECRET_KEY'],
                app.config['COOKIE_TIMEOUT'],
                request.cookies
            )
            user = User()
            user_id = user.getUID('test@tester.com', g.rdb_conn)
            self.assertTrue(logged_in_user_id == user_id)

    def test_registered_user_time_attribue(self):
        # Ensure that a registered user has creation_time attribute
        with self.client:
            response = self.client.post('/signup', data=dict(
                email='test@user.com',
                company="test",
                contact="test",
                password='test_user',
                confirm='test_user'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            user = User()
            user = user.get('username', 'test@tester.com', g.rdb_conn)
            self.assertTrue(user.creation_time)

    def test_password_hashing_is_random(self):
        # Ensure that a password salt/hash is random
        user_one = User()
        user_two = User()
        password_one = user_one.createPass("test")
        password_two = user_two.createPass("test")
        self.assertTrue(password_one != password_two)

    def test_initial_permissions(self):
        # Ensure initial permissions are set correctly
        user = User()
        user_test = user.get('username', 'test@tester.com', g.rdb_conn)
        self.assertTrue(user_test.acttype == "lite-v2")
        self.assertFalse(user_test.acttype == "pro")


if __name__ == '__main__':
    unittest.main()
