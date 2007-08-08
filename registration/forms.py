"""
Forms and validation code for user registration.

"""


import re

from django import newforms as forms
from django.contrib.auth.models import User

from registration.models import RegistrationProfile


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary.
attrs_dict = { 'class': 'required' }


username_re = re.compile(r'^\w+$')


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the password is entered twice and matches,
    and that the username is not already taken.
    
    """
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs=attrs_dict),
                               label=u'Username')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=200)),
                             label=u'Email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=u'Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=u'Password (again, to catch typos)')
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=u'I have read and agree to the Terms of Service')
    
    def clean_username(self):
        """
        Validates that the username is alphanumeric and is not already
        in use.
        
        """
        if 'username' in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
            try:
                user = User.objects.get(username__exact=self.cleaned_data['username'])
            except User.DoesNotExist:
                return self.cleaned_data['username']
            raise forms.ValidationError(u'This username is already taken. Please choose another.')
    
    def clean_password2(self):
        """
        Validates that the two password inputs match.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and \
           self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(u'You must type the same password each time')
    
    def clean_tos(self):
        """
        Validates that the user accepted the Terms of Service.
        
        """
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(u'You must agree to the terms to register')

    def save(self, profile_callback):
        """
        Creates the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.

        """
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    profile_callback=profile_callback)
        return new_user


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validates that the supplied email address is unique for the
        site.
        
        """
        if 'email' in self.cleaned_data:
            try:
                user = User.objects.get(email__exact=self.cleaned_data['email'])
            except User.DoesNotExist:
                return self.cleaned_data['email']
            raise forms.ValidationError(u'This email address is already in use. Please supply a different email address.')


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.

    To change the list of banned domains, override the attribute
    ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'live.com', 'msn.com', 'mail.ru']
    
    def clean_email(self):
        """
        Checks the supplied email address against a list of known free
        webmail domains.
        
        """
        if 'email' in self.cleaned_data:
            email_domain = self.cleaned_data['email'].split('@')[1]
            if email_domain in self.bad_domains:
                raise forms.ValidationError(u'Registration using free email addresses is prohibited. Please supply a different email address.')
            return self.cleaned_data['email']
