######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - monitors
######################################################################


import unittest
import datetime
import rethinkdb as r

from flask import g

from base import BaseTestCase


class MonitorTests(BaseTestCase):

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

    def test_user_can_edit_monitor(self):
        # Ensure that a logged in user can edit an existing monitor.
        timestamp = str(datetime.datetime.now())
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            self.client.post(
                '/dashboard/monitors/cr-api',
                data=dict(name=timestamp),
                follow_redirects=True
            )
            results = r.table('monitors').filter(
                {'name': timestamp}).run(g.rdb_conn)
            for result in results:
                monitor_id = result['id']
                break
            new_timestamp = str(datetime.datetime.now())
            response = self.client.post(
                '/dashboard/edit-monitors/cr-api/{0}'.format(monitor_id),
                data=dict(name=new_timestamp),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('Monitor &#34;{0}&#34; successfully edited'
                .format(new_timestamp), response.data)

    def test_user_can_update_monitor(self):
        # Ensure that a logged in user can update an existing monitor.
        timestamp = str(datetime.datetime.now())
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            self.client.post(
                '/dashboard/monitors/cr-api',
                data=dict(name=timestamp),
                follow_redirects=True
            )
            results = r.table('monitors').filter(
                {'name': timestamp}).run(g.rdb_conn)
            for result in results:
                monitor_id = result['id']
                break
            response = self.client.get(
                '/dashboard/action-checks/{0}/false'.format(monitor_id),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('Health check status change is queued.',
                          response.data)

    def test_user_can_delete_monitor(self):
        # Ensure that a logged in user can delete an existing monitor.
        timestamp = str(datetime.datetime.now())
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            self.client.post(
                '/dashboard/monitors/cr-api',
                data=dict(name=timestamp),
                follow_redirects=True
            )
            results = r.table('monitors').filter(
                {'name': timestamp}).run(g.rdb_conn)
            for result in results:
                monitor_id = result['id']
                break
            response = self.client.get(
                '/dashboard/delete-checks/{0}'.format(monitor_id),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('Health Check was successfully deleted.',
                          response.data)


if __name__ == '__main__':
    unittest.main()
