import unittest
from flask.ext.testing import TestCase
from web import app


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        return app


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that /dashboard requires user login
    def test_dashboard_route_login(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn('Login', response.data)


class UserViewsTests(BaseTestCase):

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn('Login', response.data)


if __name__ == '__main__':
    unittest.main()
