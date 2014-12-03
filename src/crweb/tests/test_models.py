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


if __name__ == '__main__':
    unittest.main()
