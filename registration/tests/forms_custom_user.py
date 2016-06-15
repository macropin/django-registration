from __future__ import unicode_literals
try:
    from importlib import reload  # Python 3.4+
except ImportError:
    try:
        from imp import reload  # Python 3.3
    except:
        pass  # Python 2 reload()


from django.conf import settings
from django.test import TestCase

from registration import forms
from registration.users import UsernameField


class RegistrationFormTests(TestCase):
    """
    Test the default registration forms.

    """
    def setUp(self):
        self.old_auth_model = getattr(settings, 'AUTH_USER_MODEL', None)
        settings.AUTH_USER_MODEL = 'test_app.CustomUser'
        # The form's Meta class is created on import. We have to reload()
        # to apply the new AUTH_USER_MODEL to the Meta class.
        reload(forms)

    def tearDown(self):
        settings.AUTH_USER_MODEL = self.old_auth_model

    def test_registration_form_adds_custom_user_name_field(self):
        """
        Test that ``RegistrationForm`` adds custom username
        field and does not raise errors

        """

        form = forms.RegistrationForm()

        self.assertTrue(UsernameField() in form.fields)

    def test_registration_form_subclass_is_valid(self):
        """
        Test that ``RegistrationForm`` subclasses can save

        """
        data = {'new_field': 'custom username',
                'email': 'foo@example.com',
                'password1': 'foo',
                'password2': 'foo'}

        form = forms.RegistrationForm(data=data)

        self.assertTrue(form.is_valid())
