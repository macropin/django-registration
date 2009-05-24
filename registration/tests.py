"""
Unit tests for django-registration.

"""

from django.core import mail
from django.test import TestCase


class DefaultBackendTestCase(TestCase):
    """
    Test the default registration backend.
    
    """
    def setUp(self):
        """
        Create an instance of the default backend for use in testing.
        
        """
        from registration.backends.default import DefaultBackend
        self.backend = DefaultBackend()

    def test_registration(self):
        """
        Create a new user, verifying that username, email and password
        are set correctly and that the new user is inactive and
        received an activation email.
        
        """
        new_user = self.backend.register({}, 'bob', 'secret', 'bob@example.com')
        self.assertEqual(new_user.username, 'bob')
        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')
        self.failIf(new_user.is_active)
        self.assertEqual(len(mail.outbox), 1)
