import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from registration import forms
from registration.models import RegistrationProfile


class BackendRetrievalTests(TestCase):
    """
    Test that utilities for retrieving the active backend work
    properly.

    """
    def test_get_backend(self):
        """
        Set ``REGISTRATION_BACKEND`` temporarily, then verify that
        ``get_backend()`` returns the correct value.

        """
        from registration import get_backend
        from registration.backends.default import DefaultBackend

        old_backend = getattr(settings, 'REGISTRATION_BACKEND', None)

        settings.REGISTRATION_BACKEND = 'registration.backends.default.DefaultBackend'
        self.failUnless(isinstance(get_backend(), DefaultBackend))

        settings.REGISTRATION_BACKEND = old_backend

    def test_backend_error_none(self):
        """
        Test that an invalid value for the ``REGISTRATION_BACKEND``
        setting raises the correct exception.

        """
        from registration import get_backend

        old_backend = getattr(settings, 'REGISTRATION_BACKEND', None)

        settings.REGISTRATION_BACKEND = None
        self.assertRaises(ImproperlyConfigured, get_backend)

        settings.REGISTRATION_BACKEND = old_backend

    def test_backend_error_invalid(self):
        """
        Test that a nonexistent/unimportable backend raises the
        correct exception.

        """
        from registration import get_backend

        old_backend = getattr(settings, 'REGISTRATION_BACKEND', None)

        settings.REGISTRATION_BACKEND = 'registration.backends.doesnotexist.NonExistentBackend'
        self.assertRaises(ImproperlyConfigured, get_backend)

        settings.REGISTRATION_BACKEND = old_backend


class DefaultRegistrationBackendTests(TestCase):
    """
    Test the default registration backend.

    Running these tests successfull will require two templates to be
    created for the sending of activation emails; details on these
    templates and their contexts may be found in the documentation for
    the default backend.

    """
    def setUp(self):
        """
        Create an instance of the default backend for use in testing,
        and set ``ACCOUNT_ACTIVATION_DAYS``.

        """
        from registration.backends.default import DefaultBackend
        self.backend = DefaultBackend()
        self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        settings.ACCOUNT_ACTIVATION_DAYS = 7

    def tearDown(self):
        """
        Restore the original value of ``ACCOUNT_ACTIVATION_DAYS``.

        """
        settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation

    def test_registration(self):
        """
        Test the registration process: registration creates a new
        inactive account and a new profile with activation key,
        populates the correct account data and sends an activation
        email.

        """
        new_user = self.backend.register({},
                                         username='bob',
                                         email='bob@example.com',
                                         password1='secret')

        # Details of the returned user must match what went in.
        self.assertEqual(new_user.username, 'bob')
        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')

        # New user must not be active.
        self.failIf(new_user.is_active)

        # A registration profile was created, and an activation email
        # was sent.
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_valid_activation(self):
        """
        Test the activation process: activating within the permitted
        window sets the account's ``is_active`` field to ``True`` and
        resets the activation key.

        """
        valid_user = self.backend.register({},
                                           username='alice',
                                           email='alice@example.com',
                                           password1='swordfish')

        valid_profile = RegistrationProfile.objects.get(user=valid_user)
        activated = self.backend.activate({}, valid_profile.activation_key)
        self.assertEqual(activated.username, valid_user.username)
        self.failUnless(activated.is_active)

        # Fetch the profile again to verify its activation key has
        # been reset.
        valid_profile = RegistrationProfile.objects.get(user=valid_user)
        self.assertEqual(valid_profile.activation_key,
                         RegistrationProfile.ACTIVATED)

    def test_invalid_activation(self):
        """
        Test the activation process: trying to activate outside the
        permitted window fails, and leaves the account inactive.

        """
        expired_user = self.backend.register({},
                                             username='bob',
                                             email='bob@example.com',
                                             password1='secret')

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
        old_allowed = getattr(settings, 'REGISTRATION_OPEN', True)
        settings.REGISTRATION_OPEN = True
        self.failUnless(self.backend.registration_allowed({}))

        settings.REGISTRATION_OPEN = False
        self.failIf(self.backend.registration_allowed({}))
        settings.REGISTRATION_OPEN = old_allowed

    def test_form_class(self):
        """
        Test that the default form class returned is
        ``registration.forms.RegistrationForm``.

        """
        self.failUnless(self.backend.get_form_class({}) is forms.RegistrationForm)

    def test_post_registration_redirect(self):
        """
        Test that the default post-registration redirect is the named
        pattern ``registration_complete``.

        """
        self.assertEqual(self.backend.post_registration_redirect({}, User()),
                         'registration_complete')
