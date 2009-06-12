"""
Unit tests for django-registration.

These tests assume that you have a project set up, with
``registration`` in ``INSTALLED_APPS`` and with the default templates
required by both the registration/activation views and the default
backend.

"""

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.test import TestCase

from registration import forms
from registration.models import RegistrationProfile


class RegistrationFormTests(TestCase):
    """
    Test the default registration forms.

    """
    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.

        """
        # Create a user so we can verify that duplicate usernames aren't
        # permitted.
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        invalid_data_dicts = [
            # Non-alphanumeric username.
            {'data': {'username': 'foo/bar',
                      'email': 'foo@example.com',
                      'password1': 'foo',
                      'password2': 'foo'},
            'error': ('username', [u"This value must contain only letters, numbers and underscores."])},
            # Already-existing username.
            {'data': {'username': 'alice',
                      'email': 'alice@example.com',
                      'password1': 'secret',
                      'password2': 'secret'},
            'error': ('username', [u"This username is already taken. Please choose another."])},
            # Mismatched passwords.
            {'data': {'username': 'foo',
                      'email': 'foo@example.com',
                      'password1': 'foo',
                      'password2': 'bar'},
            'error': ('__all__', [u"You must type the same password each time"])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = forms.RegistrationForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        form = forms.RegistrationForm(data={'username': 'foo',
                                            'email': 'foo@example.com',
                                            'password1': 'foo',
                                            'password2': 'foo'})
        self.failUnless(form.is_valid())

    def test_registration_form_tos(self):
        """
        Test that ``RegistrationFormTermsOfService`` requires
        agreement to the terms of service.

        """
        form = forms.RegistrationFormTermsOfService(data={'username': 'foo',
                                                          'email': 'foo@example.com',
                                                          'password1': 'foo',
                                                          'password2': 'foo'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['tos'], [u"You must agree to the terms to register"])

        form = forms.RegistrationFormTermsOfService(data={'username': 'foo',
                                                          'email': 'foo@example.com',
                                                          'password1': 'foo',
                                                          'password2': 'foo',
                                                          'tos': 'on'})
        self.failUnless(form.is_valid())

    def test_registration_form_unique_email(self):
        """
        Test that ``RegistrationFormUniqueEmail`` validates uniqueness
        of email addresses.

        """
        # Create a user so we can verify that duplicate addresses
        # aren't permitted.
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        form = forms.RegistrationFormUniqueEmail(data={'username': 'foo',
                                                       'email': 'alice@example.com',
                                                       'password1': 'foo',
                                                       'password2': 'foo'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'], [u"This email address is already in use. Please supply a different email address."])

        form = forms.RegistrationFormUniqueEmail(data={'username': 'foo',
                                                       'email': 'foo@example.com',
                                                       'password1': 'foo',
                                                       'password2': 'foo'})
        self.failUnless(form.is_valid())

    def test_registration_form_no_free_email(self):
        """
        Test that ``RegistrationFormNoFreeEmail`` disallows
        registration with free email addresses.

        """
        base_data = {'username': 'foo',
                     'password1': 'foo',
                     'password2': 'foo'}
        for domain in forms.RegistrationFormNoFreeEmail.bad_domains:
            invalid_data = base_data.copy()
            invalid_data['email'] = u"foo@%s" % domain
            form = forms.RegistrationFormNoFreeEmail(data=invalid_data)
            self.failIf(form.is_valid())
            self.assertEqual(form.errors['email'], [u"Registration using free email addresses is prohibited. Please supply a different email address."])

        base_data['email'] = 'foo@example.com'
        form = forms.RegistrationFormNoFreeEmail(data=base_data)
        self.failUnless(form.is_valid())


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


class RegistrationViewTests(TestCase):
    """
    Test the registration views.

    """
    urls = 'registration.backends.default.urls'

    def setUp(self):
        """
        Set ``REGISTRATION_BACKEND`` to the default backend, and store
        the original value to be restored later.

        """
        self.old_backend = getattr(settings, 'REGISTRATION_BACKEND', None)
        settings.REGISTRATION_BACKEND = 'registration.backends.default.DefaultBackend'
        self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
        settings.ACCOUNT_ACTIVATION_DAYS = 7

    def tearDown(self):
        """
        Retore the original value of ``REGISTRATION_BACKEND``.

        """
        settings.REGISTRATION_BACKEND = self.old_backend
        settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation

    def test_registration_view_initial(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        response = self.client.get(reverse('registration_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'registration/registration_form.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.RegistrationForm))

    def test_registration_view_success(self):
        """
        A ``POST`` to the ``register`` view with valid data properly
        creates a new user and issues a redirect.

        """
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish'})
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('registration_complete'))
        self.assertEqual(len(mail.outbox), 1)

    def test_registration_view_failure(self):
        """
        A ``POST`` to the ``register`` view with invalid data does not
        create a user, and displays appropriate error messages.

        """
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'bob',
                                          'email': 'bobe@example.com',
                                          'password1': 'foo',
                                          'password2': 'bar'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None,
                             errors=u'You must type the same password each time')
        self.assertEqual(len(mail.outbox), 0)

    def test_registration_view_closed(self):
        """
        Any attempt to access the ``register`` view when registration
        is closed fails and redirects.

        """
        old_allowed = getattr(settings, 'REGISTRATION_OPEN', True)
        settings.REGISTRATION_OPEN = False

        closed_redirect = 'http://testserver%s' % reverse('registration_disallowed')

        response = self.client.get(reverse('registration_register'))
        self.assertRedirects(response, closed_redirect)

        # Even if valid data is posted, it still shouldn't work.
        response = self.client.post(reverse('registration_register'),
                                    data={'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish'})
        self.assertRedirects(response, closed_redirect)
        self.assertEqual(RegistrationProfile.objects.count(), 0)

        settings.REGISTRATION_OPEN = old_allowed

    def test_valid_activation(self):
        """
        Test that the ``activate`` view properly handles a valid
        activation (in this case, based on the default backend's
        activation window).

        """
        # First, register an account.
        self.client.post(reverse('registration_register'),
                         data={'username': 'alice',
                               'email': 'alice@example.com',
                               'password1': 'swordfish',
                               'password2': 'swordfish'})
        profile = RegistrationProfile.objects.get(user__username='alice')

        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'registration/activate.html')
        self.failUnless(isinstance(response.context['account'],
                                   User))
        self.assertEqual(response.context['account'].username,
                         u'alice')
        self.failUnless(User.objects.get(username='alice').is_active)

    def test_invalid_activation(self):
        """
        Test that the ``activate`` view properly handles an invalid
        activation (in this case, based on the default backend's
        activation window).

        """
        # Register an account and reset its date_joined to be outside
        # the activation window.
        self.client.post(reverse('registration_register'),
                         data={'username': 'bob',
                               'email': 'bob@example.com',
                               'password1': 'secret',
                               'password2': 'secret'})
        expired_user = User.objects.get(username='bob')
        expired_user.date_joined = expired_user.date_joined - datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        expired_user.save()

        expired_profile = RegistrationProfile.objects.get(user=expired_user)
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': expired_profile.activation_key}))
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['account'])
        self.failIf(User.objects.get(username='bob').is_active)
