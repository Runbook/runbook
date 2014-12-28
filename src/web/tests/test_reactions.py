######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - reactions
######################################################################

import datetime
import unittest
import rethinkdb as r

from flask import g

from base import BaseTestCase


class ReactionTests(BaseTestCase):

    def test_dashboard_reactions_route_login(self):
        # Ensure that /dashboard/reactions requires user login.
        response = self.client.get(
            '/dashboard/reactions', follow_redirects=True)
        self.assertIn('Login', response.data)
        self.assertIn('Please Login.', response.data)

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

    def test_user_can_access_reaction(self):
        # Ensure that a logged in user can access a reaction.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get(
                '/dashboard/reactions/enotify',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Email Notification', response.data)

    def test_user_can_access_reaction_login(self):
        # Ensure that a reaction requires user login.
        with self.client:
            response = self.client.get(
                '/dashboard/reactions/enotify',
                follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Login', response.data)
            self.assertIn('Please Login.', response.data)

    def test_user_can_add_reaction(self):
        # Ensure that a logged in user can add a reaction.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.post(
                '/dashboard/reactions/enotify',
                data=dict(name="test", trigger=1,
                          frequency=1, email="test@tester.com",
                          send_true=True),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                'Reaction &#34;test&#34; successfully added.', response.data)

    def test_user_can_edit_reaction(self):
        # Ensure that a logged in user can edit an existing reaction.
        timestamp = str(datetime.datetime.now())
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            self.client.post(
                '/dashboard/reactions/enotify',
                data=dict(name=timestamp, trigger=1,
                          frequency=1, email="test@tester.com",
                          send_true=True),
                follow_redirects=True
            )
            results = r.table('reactions').filter(
                {'name': timestamp}).run(g.rdb_conn)
            for result in results:
                reaction_id = result['id']
                break
            new_timestamp = str(datetime.datetime.now())
            response = self.client.post(
                '/dashboard/edit-reactions/enotify/{0}'.format(reaction_id),
                data=dict(name=new_timestamp, trigger=1,
                          frequency=1, email="test@tester.com",
                          send_true=True),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('Reaction successfully edited.'.format(
                new_timestamp), response.data)

if __name__ == '__main__':
    unittest.main()
