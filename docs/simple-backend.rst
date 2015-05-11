.. _simple-backend:
.. module:: registration.backends.simple

The "simple" (one-step) backend
===============================

As an alternative to :ref:`the default backend <default-backend>`, and
an example of writing alternate workflows, |project| bundles
a one-step registration system in
``registration.backend.simple``. This backend's workflow is
deliberately as simple as possible:

1. A user signs up by filling out a registration form.

2. The user's account is created and is active immediately, with no
   intermediate confirmation or activation step.

3. The new user is logged in immediately.


Configuration
-------------

To use this backend, simply include the URLconf
``registration.backends.simple.urls`` somewhere in your site's own URL
configuration. For example::

    (r'^accounts/', include('registration.backends.simple.urls')),

No additional settings are required, but one optional setting is
supported:

``REGISTRATION_OPEN``
    A boolean (either ``True`` or ``False``) indicating whether
    registration of new accounts is currently permitted. A default of
    ``True`` will be assumed if this setting is not supplied.

Upon successful registration, the default redirect is to the
``registration_complete`` view (at ``accounts/register/complete/``).

The default form class used for account registration will be
:class:`registration.forms.RegistrationForm`, although this can be
overridden by supplying a custom URL pattern for the registration view
and passing the keyword argument ``form_class``, or by subclassing
``registration.backends.simple.views.RegistrationView`` and either
overriding ``form_class`` or implementing
:meth:`~registration.views.RegistrationView.get_form_class()`.
