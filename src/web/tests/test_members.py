######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - members
######################################################################


import unittest

from base import BaseTestCase


class MemberTests(BaseTestCase):

    def test_dashboard_route_login(self):
        # Ensure that /dashboard requires user login.
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn('Login', response.data)
        self.assertIn('Please Login.', response.data)

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

    def test_dashboard_subscription_route(self):
        # Ensure registered user can access dashboard/mod-subscription route.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get(
                '/dashboard/mod-subscription', follow_redirects=True)
            self.assertTrue(response.status_code == 200)
            self.assertIn('Upgrade your subscription', response.data)

    def test_dashboard_subscription_route_login(self):
        # Ensure that dashboard/mod-subscription requires user login.
        response = self.client.get(
            '/dashboard/mod-subscription', follow_redirects=True)
        self.assertIn('Login', response.data)
        self.assertIn('Please Login.', response.data)

    def test_dashboard_preferences_route(self):
        # Ensure registered user can access dashboard/user-preferences route.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get(
                '/dashboard/user-preferences', follow_redirects=True)
            self.assertTrue(response.status_code == 200)
            self.assertIn('User Preferences', response.data)

    def test_dashboard_preferences_route_login(self):
        # Ensure that dashboard/user-preferences requires user login.
        response = self.client.get(
            '/dashboard/user-preferences', follow_redirects=True)
        self.assertIn('Login', response.data)
        self.assertIn('Please Login.', response.data)

    def test_password_change_success(self):
        # Ensure user can update password.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.post(
                '/dashboard/user-preferences',
                data=dict(password="tester678", confirm="tester678"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertIn('Password successfully changed.', response.data)


if __name__ == '__main__':
    unittest.main()
