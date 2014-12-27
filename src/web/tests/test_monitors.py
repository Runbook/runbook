######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - functional (monitors blueprint)
######################################################################


import unittest

from base import BaseTestCase


class FunctionalMonitorTests(BaseTestCase):

    def test_dashboard_monitors_route_login(self):
        # Ensure that /dashboard/monitors requires user login.
        response = self.client.get('/dashboard/monitors', follow_redirects=True)
        self.assertIn('Login', response.data)
        self.assertIn('Please Login.', response.data)

    def test_dashboard_monitor_route(self):
        # Ensure registered user can access dashboard/monitor route.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get(
                '/dashboard/monitors', follow_redirects=True)
            self.assertTrue(response.status_code == 200)
            self.assertIn('Create Monitors', response.data)

    def test_user_can_access_monitor(self):
        # Ensure that a logged in user can access a monitor.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get(
                '/dashboard/monitors/cr-api',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Runbook Webhooks', response.data)

    def test_user_can_access_monitor_login(self):
        # Ensure that a monitor requires user login.
        with self.client:
            response = self.client.get(
                '/dashboard/monitors/cr-api',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Login', response.data)
            self.assertIn('Please Login.', response.data)

    def test_user_can_add_monitor(self):
        # Ensure that a logged in user can add a monitor.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.post(
                '/dashboard/monitors/cr-api',
                data=dict(name="test"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                'Monitor &#34;test&#34; successfully added.', response.data)


if __name__ == '__main__':
    unittest.main()
