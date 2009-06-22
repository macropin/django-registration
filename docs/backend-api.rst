.. _backend-api:

User registration backends
==========================

At its core, django-registration is built around the idea of pluggable
backends which can implement different workflows for user
registration. Although the default backend uses a common two-phase
system (registration followed by activation), backends are generally
free to implement any workflow desired by their authors.

This is deliberately meant to be complementary to Django's own
`pluggable authentication backends
<http://docs.djangoproject.com/en/dev/topics/auth/#other-authentication-sources>`_;
a site which uses an OpenID authentication backend, for example, can
and should make use of a registration backend which handles signups
via OpenID. And, like a Django authentication backend, a registration
backend is simply a class which implements a particular standard API
(described below).

This allows for a great deal of flexibility in the actual workflow of
registration; backends can, for example, implement any of the
following (not an exhaustive list):

* One-step (register, and done) or two-step (register and activate)
  signup.

* Invitation-based registration.

* Selectively allowing or disallowing registration (e.g., by requiring
  particular credentials to register).

* Enabling/disabling registration entirely.

* Registering via sources other than a standard username/password,
  such as OpenID.

* Selective customization of the registration process (e.g., using
  different forms or imposing different requirements for different
  types of users).


Specifying the backend to use
-----------------------------

To determine which backend to use, django-registration consult the
setting ``REGISTRATION_BACKEND``, which should be the full dotted
Python import path (as a string) of the class to be used as the
registration backend. For example, the default backend provided is in
``registration.backends.default``, implemented as a class named
``DefaultBackend``; thus, it would be enabled in a Django settings
file like so::

    REGISTRATION_BACKEND = "registration.backends.default.DefaultBackend"

If no backend is specified, if the specified module is not found or if
it does not contain a class of the appropriate name,
django-registration will raise
``django.core.exceptions.ImproperlyConfigured`` whenever
user-registration functionality is accessed.


Backend API
-----------

To be used as a registration backend, a class must implement the
following methods. For many cases, subclassing the default backend and
selectively overriding behavior will be suitable, but for other
situations (e.g., workflows significantly different from the default)
a full implementation is needed.


register(self, request, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method implements the logic of actually creating the new user
account. Often, but not necessarily always, this will involve creating
an instance of ``django.contrib.auth.models.User`` from the supplied
data.

This method will only be called after a signup form has been
displayed, and the data collected by the form has been properly
validated.

Arguments to this method are:

``request``
    The Django `HttpRequest
    <http://docs.djangoproject.com/en/dev/ref/request-response/#httprequest-objects>`_
    object in which a new user is attempting to register.

``**kwargs``
    A dictionary of the ``cleaned_data`` from the signup form.

After creating the new user account, this method should create or
obtain an instance of ``django.contrib.auth.models.User`` representing
that account. It should then send the signal
``registration.signals.user_registered``, with two arguments:

``sender``
    The backend class (e.g., ``self.__class__``).

``user``
    The ``User`` instance representing the new account.

Finally, this method should return the ``User`` instance.


activate(self, request, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For workflows which require a separate activation step, this method
should implement the necessary logic for account activation.

Arguments to this method are:

``request``
    The Django ``HttpRequest`` object in which the account is being
    activated.

``**kwargs``
    A dictionary of any additional arguments (e.g., information
    captured from the URL, such as an activation key) received by the
    activation view. The combination of the ``HttpRequest`` and this
    additional information must be sufficient to identify the account
    which will be activated.

If the account cannot be successfully activated (for example, in the
default backend if the activation period has expired), this method
should return ``False``.

If the account is successfully activated, this method should create or
obtain an instance of ``django.contrib.auth.models.User`` representing
the activated account. It should then send the signal
``registration.signals.user_activated``, with two arguments:

``sender``
    The backend class.

``user``
    The ``User`` instance representing the new account.

This method should then return the ``User`` instance.

For workflows which do not require a separate activation step, this
method can and should raise ``NotImplementedError``.


registration_allowed(self, request)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method returns a boolean value indicating whether the given
``HttpRequest`` is permitted to register a new account (``True`` if
registration is permitted, ``False`` otherwise). It may determine this
based on some aspect of the ``HttpRequest`` (e.g., the presence or
absence of an invitation code in the URL), based on a setting (in the
default backend, a setting can be used to disable registration),
information in the database or any other information it can access.

Arguments to this method are:

``request``
    The Django ``HttpRequest`` object in which a new user is
    attempting to register.

If this method returns ``False``, the registration view will not
display a form for account creation; instead, it will issue a redirect
to a URL explaining that registration is not permitted.


get_form_class(self, request)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method should return a form class -- a subclass of
``django.forms.Form`` -- suitable for use in registering users with
this backend. As such, it should collect and validate any information
required by the backend's ``register`` method.

Arguments to this method are:

``request``
    The Django ``HttpRequest`` object in which a new user is
    attempting to register.

post_registration_redirect(self, request, user)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method should return a location to which the user will be
redirected after successful registration. This should be a tuple of
``(to, args, kwargs)``, suitable for use as the arguments to `Django's
"redirect" shortcut
<http://docs.djangoproject.com/en/dev/topics/http/shortcuts/#redirect>`_.

Arguments to this method are:

``request``
    The Django ``HttpRequest`` object in which the user registered.

``user``
    The ``User`` instance representing the new user account.
