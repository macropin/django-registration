from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from registration.forms import RegistrationForm
from registration.users import UserModel


class SimpleBackendViewTests(TestCase):
    urls = 'test_app.urls_simple'

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
        Registration creates a new account and logs the user in.

        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})
        new_user = UserModel().objects.get(username='bob')
        self.assertEqual(302, resp.status_code)
        self.failUnless(reverse('registration_complete') in resp['Location'])

        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'bob@example.com')

        # New user must be active.
        self.failUnless(new_user.is_active)

        # New user must be logged in.
        resp = self.client.get(reverse('registration_register'))
        self.failUnless(resp.context['user'].is_authenticated())

    def test_registration_next_param(self):
        """
        using the next param to skip the registration_complete page
        after successful registration and target another path
        """
        # get registration view w/ form
        resp = self.client.get(
            reverse('registration_register'), {'next': '/somewhere/'})
        self.assertEqual(resp.request[u'QUERY_STRING'], 'next=%2Fsomewhere%2F')
        self.assertEqual(200, resp.status_code)
        self.assertTrue('somewhere' in resp.content)

        # fill in form and POST it
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret',
                                      'next': '/somewhere/'},
                                follow=True)
        print resp.request
        self.assertTrue('/somewhere/' in resp.request['PATH_INFO'])

    def test_registration_next_param_injection(self):
        """ attempt to use the next param to inject an alert into
        the template
        """
        with self.assertRaises(ValueError):

            resp = self.client.get(
                reverse('registration_register'),
                {'next': '"/><script>alert("boom");</script>'})

    def test_registration_next_param_bad_redirect(self):
        """
        attempt to misuse next param to go to another host
        """
        resp = self.client.post(reverse('registration_register'),
                                data={'username': 'bob',
                                      'email': 'bob@example.com',
                                      'password1': 'secret',
                                      'password2': 'secret',
                                      'next': 'http://www.google.com'},
                                follow=True)
        self.assertEqual(resp.redirect_chain, [
            ('/accounts/register/complete/', 302)])
        self.assertTrue(200, resp.status_code)
        self.assertFalse('google' in resp.request['PATH_INFO'])

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
