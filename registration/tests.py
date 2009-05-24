"""
Unit tests for django-registration.

"""

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from registration.forms import RegistrationForm
from registration.models import RegistrationProfile


class DefaultBackendTestCase(TestCase):
    """
    Test the default registration backend.

    Running these tests successfull will require two templates to be
    created for the sending of activation emails; details on these
    templates and their contexts may be found in the documentation for
    the default backend. The setting ``ACCOUNT_ACTIVATION_DAYS`` must
    also be specified, and must be an integer.
    
    """
    def setUp(self):
        """
        Create an instance of the default backend for use in testing.
        
        """
        from registration.backends.default import DefaultBackend
        self.backend = DefaultBackend()

    def test_registration(self):
        """
        Test the registration process: registration creates a new
        inactive account and a new profile with activation key,
        populates the correct account data and sends an activation
        email.
        
        """
        new_user = self.backend.register({}, 'bob', 'bob@example.com', 'secret')
        self.assertEqual(new_user.username, 'bob')
        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')
        self.failIf(new_user.is_active)
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_activation(self):
        """
        Test the activation process: activating within the permitted
        window sets the account's ``is_active`` field to ``True`` and
        resets the activation key, while failing to activate within
        the permitted window forbids later activation.
        
        """
        # First, test with a user activating inside the activation
        # window.
        valid_user = self.backend.register({}, 'alice', 'alice@example.com', 'swordfish')
        valid_profile = RegistrationProfile.objects.get(user=valid_user)
        activated = self.backend.activate({}, valid_profile.activation_key)
        self.assertEqual(activated.username, valid_user.username)
        self.failUnless(activated.is_active)

        # Fetch the profile again to verify its activation key has
        # been reset.
        valid_profile = RegistrationProfile.objects.get(user=valid_user)
        self.assertEqual(valid_profile.activation_key, RegistrationProfile.ACTIVATED)

        # Now test again, but with a user activating outside the
        # activation window.
        expired_user = self.backend.register({}, 'bob', 'bob@example.com', 'secret')
        expired_user.date_joined = expired_user.date_joined - datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        expired_user.save()
        expired_profile = RegistrationProfile.objects.get(user=expired_user)
        self.failIf(self.backend.activate({}, expired_profile.activation_key))
        self.failUnless(expired_profile.activation_key_expired())

    def test_allow(self):
        """
        Test that the setting ``REGISTRATION_OPEN`` appropriately
        controls whether registration is permitted.
        
        """
        self.failUnless(self.backend.registration_allowed({}))
        settings.REGISTRATION_OPEN = False
        self.failIf(self.backend.registration_allowed({}))

    def test_form_class(self):
        """
        Test that the default form class returned is
        ``registration.forms.RegistrationForm``.
        
        """
        self.failUnless(self.backend.get_form_class({}) is RegistrationForm)

    def test_post_registration_redirect(self):
        """
        Test that the default post-registration redirect is the named
        pattern ``registration_complete``.
        
        """
        self.assertEqual(self.backend.post_registration_redirect({}, User()),
                         'registration_complete')
