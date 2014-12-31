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
