import datetime
import hashlib
import re

from django.utils import six
from django.apps import apps
from django.conf import settings
from django.core import mail
from django.core import management
from django.test import TestCase

from registration.models import RegistrationProfile
from registration.users import UserModel

Site = apps.get_model('sites', 'Site')


class RegistrationModelTests(TestCase):
    """
    Test the model and manager used in the default backend.

    """
    user_info = {'username': 'alice',
                 'password': 'swordfish',
                 'email': 'alice@example.com'}

    def setUp(self):
        self.old_activation = getattr(settings,
                                      'ACCOUNT_ACTIVATION_DAYS', None)
        self.old_reg_email = getattr(settings,
                                     'REGISTRATION_DEFAULT_FROM_EMAIL', None)
        self.old_email_html = getattr(settings,
                                      'REGISTRATION_EMAIL_HTML', None)
        self.old_django_email = getattr(settings,
                                        'DEFAULT_FROM_EMAIL', None)

        settings.ACCOUNT_ACTIVATION_DAYS = 7
        settings.REGISTRATION_DEFAULT_FROM_EMAIL = 'registration@email.com'
        settings.REGISTRATION_EMAIL_HTML = True
        settings.DEFAULT_FROM_EMAIL = 'django@email.com'

    def tearDown(self):
        settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation
        settings.REGISTRATION_DEFAULT_FROM_EMAIL = self.old_reg_email
        settings.REGISTRATION_EMAIL_HTML = self.old_email_html
        settings.DEFAULT_FROM_EMAIL = self.old_django_email

    def test_profile_creation(self):
        """
        Creating a registration profile for a user populates the
        profile with the correct user and a SHA1 hash to use as
        activation key.

        """
        new_user = UserModel().objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)

        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertEqual(profile.user.id, new_user.id)
        self.failUnless(re.match('^[a-f0-9]{40}$', profile.activation_key))
        self.assertEqual(six.text_type(profile),
                         "Registration information for alice")

    def test_activation_email(self):
        """
        ``RegistrationProfile.send_activation_email`` sends an
        email.

        """
        new_user = UserModel().objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)
        profile.send_activation_email(Site.objects.get_current())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])

    def test_activation_email_uses_registration_default_from_email(self):
        """
        ``RegistrationProfile.send_activation_email`` sends an
        email.

        """
        new_user = UserModel().objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)
        profile.send_activation_email(Site.objects.get_current())
        self.assertEqual(mail.outbox[0].from_email, 'registration@email.com')

    def test_activation_email_falls_back_to_django_default_from_email(self):
        """
        ``RegistrationProfile.send_activation_email`` sends an
        email.

        """
        settings.REGISTRATION_DEFAULT_FROM_EMAIL = None
        new_user = UserModel().objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)
        profile.send_activation_email(Site.objects.get_current())
        self.assertEqual(mail.outbox[0].from_email, 'django@email.com')

    def test_activation_email_is_html_by_default(self):
        """
        ``RegistrationProfile.send_activation_email`` sends an html
        email by default.

        """
        new_user = UserModel().objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)
        profile.send_activation_email(Site.objects.get_current())

        self.assertEqual(len(mail.outbox[0].alternatives), 1)

    def test_activation_email_is_plain_text_if_html_disabled(self):
        """
        ``RegistrationProfile.send_activation_email`` sends a plain
        text email if settings.REGISTRATION_EMAIL_HTML is False.

        """
        settings.REGISTRATION_EMAIL_HTML = False
        new_user = UserModel().objects.create_user(**self.user_info)
        profile = RegistrationProfile.objects.create_profile(new_user)
        profile.send_activation_email(Site.objects.get_current())

        self.assertEqual(len(mail.outbox[0].alternatives), 0)

    def test_user_creation(self):
        """
        Creating a new user populates the correct data, and sets the
        user's account inactive.

        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        self.assertEqual(new_user.username, 'alice')
        self.assertEqual(new_user.email, 'alice@example.com')
        self.failUnless(new_user.check_password('swordfish'))
        self.failIf(new_user.is_active)

    def test_user_creation_email(self):
        """
        By default, creating a new user sends an activation email.

        """
        RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        self.assertEqual(len(mail.outbox), 1)

    def test_user_creation_no_email(self):
        """
        Passing ``send_email=False`` when creating a new user will not
        send an activation email.

        """
        RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(),
            send_email=False, **self.user_info)
        self.assertEqual(len(mail.outbox), 0)

    def test_unexpired_account(self):
        """
        ``RegistrationProfile.activation_key_expired()`` is ``False``
        within the activation window.

        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        profile = RegistrationProfile.objects.get(user=new_user)
        self.failIf(profile.activation_key_expired())

    def test_expired_account(self):
        """
        ``RegistrationProfile.activation_key_expired()`` is ``True``
        outside the activation window.

        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        new_user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()
        profile = RegistrationProfile.objects.get(user=new_user)
        self.failUnless(profile.activation_key_expired())

    def test_valid_activation(self):
        """
        Activating a user within the permitted window makes the
        account active, and resets the activation key.

        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        profile = RegistrationProfile.objects.get(user=new_user)
        activated = (RegistrationProfile.objects
                     .activate_user(profile.activation_key))

        self.failUnless(isinstance(activated, UserModel()))
        self.assertEqual(activated.id, new_user.id)
        self.failUnless(activated.is_active)

        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertTrue(profile.activated)

    def test_expired_activation(self):
        """
        Attempting to activate outside the permitted window does not
        activate the account.

        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        new_user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()

        profile = RegistrationProfile.objects.get(user=new_user)
        activated = (RegistrationProfile.objects
                     .activate_user(profile.activation_key))

        self.failIf(isinstance(activated, UserModel()))
        self.failIf(activated)

        new_user = UserModel().objects.get(username='alice')
        self.failIf(new_user.is_active)

        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertFalse(profile.activated)

    def test_activation_invalid_key(self):
        """
        Attempting to activate with a key which is not a SHA1 hash
        fails.

        """
        self.failIf(RegistrationProfile.objects.activate_user('foo'))

    def test_activation_already_activated(self):
        """
        Attempting to re-activate an already-activated account fails.

        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        profile = RegistrationProfile.objects.get(user=new_user)
        RegistrationProfile.objects.activate_user(profile.activation_key)

        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertEqual(RegistrationProfile.objects.activate_user(profile.activation_key), new_user)

    def test_activation_deactivated(self):
        """
        Attempting to re-activate a deactivated account fails.
        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        profile = RegistrationProfile.objects.get(user=new_user)
        RegistrationProfile.objects.activate_user(profile.activation_key)

        # Deactivate the new user.
        new_user.is_active = False
        new_user.save()

        # Try to activate again and ensure False is returned.
        failed = RegistrationProfile.objects.activate_user(profile.activation_key)
        self.assertFalse(failed)

    def test_activation_nonexistent_key(self):
        """
        Attempting to activate with a non-existent key (i.e., one not
        associated with any account) fails.

        """
        # Due to the way activation keys are constructed during
        # registration, this will never be a valid key.
        invalid_key = hashlib.sha1(six.b('foo')).hexdigest()
        self.failIf(RegistrationProfile.objects.activate_user(invalid_key))

    def test_expired_user_deletion(self):
        """
        ``RegistrationProfile.objects.delete_expired_users()`` only
        deletes inactive users whose activation window has expired.

        """
        RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        expired_user = (RegistrationProfile.objects
                        .create_inactive_user(
                            site=Site.objects.get_current(),
                            username='bob',
                            password='secret',
                            email='bob@example.com'))
        expired_user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        expired_user.save()

        RegistrationProfile.objects.delete_expired_users()
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertRaises(UserModel().DoesNotExist,
                          UserModel().objects.get, username='bob')

    def test_management_command(self):
        """
        The ``cleanupregistration`` management command properly
        deletes expired accounts.

        """
        RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), **self.user_info)
        expired_user = (RegistrationProfile.objects
                        .create_inactive_user(site=Site.objects.get_current(),
                                              username='bob',
                                              password='secret',
                                              email='bob@example.com'))
        expired_user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        expired_user.save()

        management.call_command('cleanupregistration')
        self.assertEqual(RegistrationProfile.objects.count(), 1)
        self.assertRaises(UserModel().DoesNotExist,
                          UserModel().objects.get, username='bob')

    def test_resend_activation_email(self):
        """
        Test resending activation email to an existing user
        """
        user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), send_email=False, **self.user_info)
        self.assertEqual(len(mail.outbox), 0)

        profile = RegistrationProfile.objects.get(user=user)
        orig_activation_key = profile.activation_key

        self.assertTrue(RegistrationProfile.objects.resend_activation_mail(
            email=self.user_info['email'],
            site=Site.objects.get_current(),
        ))

        profile = RegistrationProfile.objects.get(pk=profile.pk)
        new_activation_key = profile.activation_key

        self.assertNotEqual(orig_activation_key, new_activation_key)
        self.assertEqual(len(mail.outbox), 1)

    def test_resend_activation_email_nonexistent_user(self):
        """
        Test resending activation email to a nonexisting user
        """
        self.assertFalse(RegistrationProfile.objects.resend_activation_mail(
            email=self.user_info['email'],
            site=Site.objects.get_current(),
        ))
        self.assertEqual(len(mail.outbox), 0)

    def test_resend_activation_email_activated_user(self):
        """
        Test the scenario where user tries to resend activation code
        to the already activated user's email
        """
        user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), send_email=False, **self.user_info)

        profile = RegistrationProfile.objects.get(user=user)
        activated = (RegistrationProfile.objects
                     .activate_user(profile.activation_key))
        self.assertTrue(activated.is_active)

        self.assertFalse(RegistrationProfile.objects.resend_activation_mail(
            email=self.user_info['email'],
            site=Site.objects.get_current(),
        ))
        self.assertEqual(len(mail.outbox), 0)

    def test_resend_activation_email_expired_user(self):
        """
        Test the scenario where user tries to resend activation code
        to the expired user's email
        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            site=Site.objects.get_current(), send_email=False, **self.user_info)
        new_user.date_joined -= datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS + 1)
        new_user.save()

        profile = RegistrationProfile.objects.get(user=new_user)
        self.assertTrue(profile.activation_key_expired())

        self.assertFalse(RegistrationProfile.objects.resend_activation_mail(
            email=self.user_info['email'],
            site=Site.objects.get_current(),
        ))
        self.assertEqual(len(mail.outbox), 0)
