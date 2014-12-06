######################################################################
# Runbook Web Application
# -------------------------------------------------------------------
# Tests - permissions
######################################################################


import unittest

from flask import g, request

from base import BaseTestCase
from users import User
from web import app, verifyLogin


class TestUserPermissions(BaseTestCase):
    pass
