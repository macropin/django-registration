from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration.models import RegistrationProfile
from registration import signals


class ModelBasedActivationBackend(object):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.
    
    """
    def register(request, username, email, password):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.objects.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)
        user_registered.send(user=new_user)
        return new_user

    def activate(request):
        """
        Given an HTTP request with an activation key in its URL, look
        up and activate the user account corresponding to that key (if
        possible).
        
        """
        pass

    def registration_allowed(request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_ALLOWED`` is not specified in settings, or
          is set to ``True``, registration is permitted.

        * If ``REGISTRATION_ALLOWED`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        pass

    def get_form_class(request):
        """
        Return the default form class used for user registration.
        
        """
        pass
