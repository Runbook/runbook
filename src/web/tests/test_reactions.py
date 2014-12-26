######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - reactions
######################################################################


import unittest

from base import BaseTestCase


class MonitorTests(BaseTestCase):

    def test_user_can_access_reactions(self):
        # Ensure that a logged in user can access a reaction
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get(
                '/dashboard/reactions/heroku-scale-out',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Heroku: Scale Out Dynos', response.data)


if __name__ == '__main__':
    unittest.main()
