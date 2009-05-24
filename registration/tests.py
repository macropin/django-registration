"""
Unit tests for django-registration.

"""

from django.core import mail
from django.test import TestCase

from registration.models import RegistrationProfile


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

    def test_activation(self):
        """
        Test the activation process: activating within the permitted
        window sets the account's ``is_active`` field to ``True`` and
        resets the activation key, while failing to activate within
        the permitted window forbids later activation.
        
        """
        valid_user = self.backend.register({}, 'alice', 'swordfish', 'alice@example.com')
        valid_profile = RegistrationProfile.objects.get(user=valid_user)
        activated = self.backend.activate({}, valid_profile.activation_key)
        self.assertEqual(activated.username, valid_user.username)
        self.failUnless(activated.is_active)
