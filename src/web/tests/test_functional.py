######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - functional
######################################################################


import unittest

from flask import url_for, g

from base import BaseTestCase
from users import User


class FunctionalTests(BaseTestCase):

    def test_index(self):
        # Ensure that Flask was set up correctly
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('DevOps, automated', response.data)

    def test_index_url_for(self):
        # Ensure that public blueprint works correctly
        response = self.client.get(
            url_for('public.index_redirect'), content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('DevOps, automated', response.data)

    def test_dashboard_route_login(self):
        # Ensure that /dashboard requires user login
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn('Login', response.data)

    def test_dashboard_monitors_route_login(self):
        # Ensure that /dashboard/monitors requires user login
        response = self.client.get('/dashboard/monitors', follow_redirects=True)
        self.assertIn('Login', response.data)

    def test_dashboard_reactions_route_login(self):
        # Ensure that /dashboard/reactions requires user login
        response = self.client.get(
            '/dashboard/reactions', follow_redirects=True)
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

    def test_dashboard_reaction_route(self):
        # Ensure registered user can access dashboard/reaction route.
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@tester.com", password="password456"),
                follow_redirects=True
            )
            response = self.client.get(
                '/dashboard/reactions', follow_redirects=True)
            self.assertTrue(response.status_code == 200)
            self.assertIn('Create Reactions', response.data)

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


class FunctionalStaticPagesTests(BaseTestCase):

    def test_static_pages_pricing_route(self):
        # Ensure that /pages/pricig works correctly
        response = self.client.get('/pages/pricing', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Pricing', response.data)

    def test_static_pages_faq_route(self):
        # Ensure that /pages/faq works correctly
        response = self.client.get('/pages/faq', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('What is <strong>runbook.io</strong>?', response.data)

    def test_static_pages_tos_route(self):
        # Ensure that /pages/tos works correctly
        response = self.client.get('/pages/tos', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Runbook Terms of Service ("Agreement")', response.data)

    def test_static_pages_monitors_route(self):
        # Ensure that /pages/monitors works correctly
        response = self.client.get('/pages/monitors', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Available Monitors', response.data)

    def test_static_pages_reactions_route(self):
        # Ensure that /pages/reactions works correctly
        response = self.client.get('/pages/reactions', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Available Reactions', response.data)


if __name__ == '__main__':
    unittest.main()
