import datetime

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from registration.forms import RegistrationForm
from registration.backends.default.views import RegistrationView
from registration.models import RegistrationProfile
from registration.users import UserModel


class DefaultBackendViewTests(TestCase):
    """
    Test the default registration backend.

    Running these tests successfully will require two templates to be
    created for the sending of activation emails; details on these
    templates and their contexts may be found in the documentation for
    the default backend.

    """
    urls = 'test_app.urls_default'

    def setUp(self):
        """
        Create an instance of the default backend for use in testing,
        and set ``ACCOUNT_ACTIVATION_DAYS`` if it's not set already.

        """
        self.old_activation = getattr(settings,
                                      'ACCOUNT_ACTIVATION_DAYS', None)
        if self.old_activation is None:
            settings.ACCOUNT_ACTIVATION_DAYS = 7  # pragma: no cover

    def tearDown(self):
        """
        Yank ``ACCOUNT_ACTIVATION_DAYS`` back out if it wasn't
        originally set.

        """
        if self.old_activation is None:
            # pragma: no cover
            settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation

    def test_allow(self):
        """
        The setting ``REGISTRATION_OPEN`` appropriately controls
        whether registration is permitted.

        """
        old_allowed = getattr(settings, 'REGISTRATION_OPEN', True)
        settings.REGISTRATION_OPEN = True

        resp = self.client.get(reverse('registration_register'))
        self.assertEqual(200, resp.status_code)

        settings.REGISTRATION_OPEN = False

        # Now all attempts to hit the register view should redirect to
        # the 'registration is closed' message.
        resp = self.client.get(reverse('registration_register'))
        self.assertRedirects(resp, reverse('registration_disallowed'))

        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})
        self.assertRedirects(resp, reverse('registration_disallowed'))

        settings.REGISTRATION_OPEN = old_allowed

    def test_registration_get(self):
        """
        HTTP ``GET`` to the registration view uses the appropriate
        template and populates a registration form into the context.

        """
        resp = self.client.get(reverse('registration_register'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp,
                                'registration/registration_form.html')
        self.failUnless(isinstance(resp.context['form'],
                        RegistrationForm))

    def test_registration(self):
        """
        Registration creates a new inactive account and a new profile
        with activation key, populates the correct account data and
        sends an activation email.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})
        self.assertRedirects(resp, reverse('registration_complete'))

        new_user = UserModel().objects.get(username='bob')

        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')

        # New user must not be active.
        self.failIf(new_user.is_active)

        # A registration profile was created, and an activation email
        # was sent.
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_registration_no_email(self):
        """
        Overriden Registration view does not send an activation email if the
        associated class variable is set to ``False``

        """
        class RegistrationNoEmailView(RegistrationView):
            SEND_ACTIVATION_EMAIL = False

        request_factory = RequestFactory()
        view = RegistrationNoEmailView.as_view()
        view(request_factory.post('/', data={
            'username': 'bob',
            'email': 'bob@example.com',
            'password1': 'secret',
            'password2': 'secret'}))

        UserModel().objects.get(username='bob')
        # A registration profile was created, and no activation email was sent.
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(
        INSTALLED_APPS=('django.contrib.auth', 'registration',)
    )
    def test_registration_no_sites(self):
        """
        Registration still functions properly when
        ``django.contrib.sites`` is not installed; the fallback will
        be a ``RequestSite`` instance.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})
        self.assertEqual(302, resp.status_code)

        new_user = UserModel().objects.get(username='bob')

        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')

        self.failIf(new_user.is_active)

        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_registration_failure(self):
        """
        Registering with invalid data fails.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'notsecret'})
        self.assertEqual(200, resp.status_code)
        self.failIf(resp.context['form'].is_valid())
        self.assertEqual(0, len(mail.outbox))

    def test_activation(self):
        """
        Activation of an account functions properly.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})

        profile = RegistrationProfile.objects.get(user__username='bob')

        resp = self.client.get(
            reverse('registration_activate',
                    args=(),
                    kwargs={'activation_key': profile.activation_key}))
        self.assertRedirects(resp, reverse('registration_activation_complete'))

    def test_activation_expired(self):
        """
        An expired account can't be activated.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})

        profile = RegistrationProfile.objects.get(user__username='bob')
        user = profile.user
        user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS)
        user.save()

        resp = self.client.get(
            reverse('registration_activate',
                    args=(),
                    kwargs={'activation_key': profile.activation_key}))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'registration/activate.html')
        user = UserModel().objects.get(username='bob')
        self.assertFalse(user.is_active)

    def test_resend_activation(self):
        """
        Resend activation functions properly.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})

        profile = RegistrationProfile.objects.get(user__username='bob')

        resp = self.client.post(reverse('registration_resend_activation'),
                                data={'email': profile.user.email})
        self.assertTemplateUsed(resp,
                                'registration/resend_activation_complete.html')
        self.assertEqual(resp.context['email'], profile.user.email)

    def test_resend_activation_invalid_email(self):
        """
        Calling resend with an invalid email shows the same template.

        """
        resp = self.client.post(reverse('registration_resend_activation'),
                                data={'email': 'invalid@example.com'})
        self.assertTemplateUsed(resp,
                                'registration/resend_activation_complete.html')
