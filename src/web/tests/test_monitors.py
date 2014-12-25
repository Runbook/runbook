######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - monitors
######################################################################


import unittest

from base import BaseTestCase


class MonitorTests(BaseTestCase):

    def test_index(self):
        # Ensure that Flask was set up correctly
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


if __name__ == '__main__':
    unittest.main()
