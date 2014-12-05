######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - forms
######################################################################


import unittest

from base import BaseTestCase
from user.forms import LoginForm, SignupForm


class TestLoginForm(BaseTestCase):

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='ad@min.com', password='admin')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())


class TestSignupForm(BaseTestCase):

    def test_validate_success_register_form(self):
        # Ensure correct data validates.
        form = SignupForm(
            email='test@signupform.com',
            company="test",
            contact="test",
            password='signupformtest',
            confirm='signupformtest')
        self.assertTrue(form.validate())

    def test_validate_invalid_password_format(self):
        # Ensure incorrect data does not validate.
        form = SignupForm(
            email='test@signupform.com',
            company="test",
            contact="test",
            password='short',
            confirm='signupformtest')
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register when a duplicate email is used
        form = SignupForm(
            email='test@tester.com',
            company="test",
            contact="test",
            password='short',
            confirm='signupformtest')
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
