.. _simple-backend:
.. module:: registration.backends.simple

The "simple" (one-step) backend
===============================

As an alternative to :ref:`the default backend <default-backend>`, and
an example of writing :ref:`registration backends <backend-api>`,
django-registration bundles a one-step registration system in
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

Upon successful registration, the default redirect is to the URL
specified by the ``get_absolute_url()`` method of the newly-created
``User`` object; by default, this will be ``/users/<username>/``,
although it can be overridden in either of two ways:

1. Specify a custom URL pattern for the
   :func:`~registration.views.register` view, passing the keyword
   argument ``success_url``.

2. Override the default ``get_absolute_url()`` of the ``User`` model
   in your Django configuration, as covered in `Django's settings
   documentation
   <http://docs.djangoproject.com/en/dev/ref/settings/#absolute-url-overrides>`_.

The default form class used for account registration will be
:class:`registration.forms.RegistrationForm`, although this can be
overridden by supplying a custom URL pattern for the ``register()``
view and passing the keyword argument ``form_class``.

Note that because this backend does not use an activation step,
attempting to use the :func:`~registration.views.activate` view with
this backend or calling the backend's ``activate()`` or
``post_activation_redirect()`` methods will raise
``NotImplementedError``.
