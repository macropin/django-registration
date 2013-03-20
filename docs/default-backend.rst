.. _default-backend:
.. module:: registration.backends.default

The default backend
===================

A default registration backend` is bundled with django-registration,
as the module ``registration.backends.default``, and implements a
simple two-step workflow in which a new user first registers, then
confirms and activates the new account by following a link sent to the
email address supplied during registration.


Default behavior and configuration
----------------------------------

To make use of this backend, simply include the URLConf
``registration.backends.default.urls`` at whatever location you choose
in your URL hierarchy.

This backend makes use of the following settings:

``ACCOUNT_ACTIVATION_DAYS``
    This is the number of days users will have to activate their
    accounts after registering. Failing to activate during that period
    will leave the account inactive (and possibly subject to
    deletion). This setting is required, and must be an integer.

``REGISTRATION_OPEN``
    A boolean (either ``True`` or ``False``) indicating whether
    registration of new accounts is currently permitted. This setting
    is optional, and a default of ``True`` will be assumed if it is
    not supplied.

By default, this backend uses
:class:`registration.forms.RegistrationForm` as its form class for
user registration; this can be overridden by passing the keyword
argument ``form_class`` to the :func:`~registration.views.register`
view.

Two views are provided:
``registration.backends.default.views.RegistrationView`` and
``registration.backends.default.views.ActivationView``. These views
subclass django-registration's base
:class:`~registration.views.RegistrationView` and
:class:`~registration.views.ActivationView`, respectively, and
implement the two-step registration/activation process.

Upon successful registration -- not activation -- the default redirect
is to the URL pattern named ``registration_complete``; this can be
overridden in subclasses by changing
:attr:`~registration.views.RegistrationView.success_url` or
implementing
:meth:`~registration.views.RegistrationView.get_success_url()`

Upon successful activation, the default redirect is to the URL pattern
named ``registration_activation_complete``; this can be overridden in
subclasses by implementing
:meth:`~registration.views.ActivationView.get_success_url()`.


How account data is stored for activation
-----------------------------------------

During registration, a new instance of
``django.contrib.auth.models.User`` is created to represent the new
account, with the ``is_active`` field set to ``False``. An email is
then sent to the email address of the account, containing a link the
user must click to activate the account; at that point the
``is_active`` field is set to ``True``, and the user may log in
normally.

Activation is handled by generating and storing an activation key in
the database, using the following model:


.. currentmodule:: registration.models

.. class:: RegistrationProfile

   A simple representation of the information needed to activate a new
   user account. This is **not** a user profile; it simply provides a
   place to temporarily store the activation key and determine whether
   a given account has been activated.

   Has the following fields:

   .. attribute:: user

      A ``ForeignKey`` to ``django.contrib.auth.models.User``,
      representing the user account for which activation information
      is being stored.

   .. attribute:: activation_key

      A 40-character ``CharField``, storing the activation key for the
      account. Initially, the activation key is the hexdigest of a
      SHA1 hash; after activation, this is reset to :attr:`ACTIVATED`.

   Additionally, one class attribute exists:

   .. attribute:: ACTIVATED

      A constant string used as the value of :attr:`activation_key`
      for accounts which have been activated.

   And the following methods:

   .. method:: activation_key_expired()

      Determines whether this account's activation key has expired,
      and returns a boolean (``True`` if expired, ``False``
      otherwise). Uses the following algorithm:

      1. If :attr:`activation_key` is :attr:`ACTIVATED`, the account
         has already been activated and so the key is considered to
         have expired.

      2. Otherwise, the date of registration (obtained from the
         ``date_joined`` field of :attr:`user`) is compared to the
         current date; if the span between them is greater than the
         value of the setting ``ACCOUNT_ACTIVATION_DAYS``, the key is
         considered to have expired.

      :rtype: bool

   .. method:: send_activation_email(site)

      Sends an activation email to the address of the account.

      The activation email will make use of two templates:
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which are used for the
      subject of the email and the body of the email,
      respectively. Each will receive the following context:

      ``activation_key``
          The value of :attr:`activation_key`.

      ``expiration_days``
          The number of days the user has to activate, taken from the
          setting ``ACCOUNT_ACTIVATION_DAYS``.

      ``site``
          An object representing the site on which the account was
          registered; depending on whether ``django.contrib.sites`` is
          installed, this may be an instance of either
          ``django.contrib.sites.models.Site`` (if the sites
          application is installed) or
          ``django.contrib.sites.models.RequestSite`` (if
          not). Consult `the documentation for the Django sites
          framework
          <http://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_
          for details regarding these objects' interfaces.

      Because email subjects must be a single line of text, the
      rendered output of ``registration/activation_email_subject.txt``
      will be forcibly condensed to a single line.

      :param site: An object representing the site on which account
         was registered.
      :type site: ``django.contrib.sites.models.Site`` or
        ``django.contrib.sites.models.RequestSite``
      :rtype: ``None``


Additionally, :class:`RegistrationProfile` has a custom manager
(accessed as ``RegistrationProfile.objects``):


.. class:: RegistrationManager

   This manager provides several convenience methods for creating and
   working with instances of :class:`RegistrationProfile`:

   .. method:: activate_user(activation_key)

      Validates ``activation_key`` and, if valid, activates the
      associated account by setting its ``is_active`` field to
      ``True``. To prevent re-activation of accounts, the
      :attr:`~RegistrationProfile.activation_key` of the
      :class:`RegistrationProfile` for the account will be set to
      :attr:`RegistrationProfile.ACTIVATED` after successful
      activation.

      Returns the ``User`` instance representing the account if
      activation is successful, ``False`` otherwise.

      :param activation_key: The activation key to use for the
         activation.
      :type activation_key: string, a 40-character SHA1 hexdigest
      :rtype: ``User`` or bool

   .. method:: delete_expired_users

      Removes expired instances of :class:`RegistrationProfile`, and
      their associated user accounts, from the database. This is
      useful as a periodic maintenance task to clean out accounts
      which registered but never activated.

      Accounts to be deleted are identified by searching for instances
      of :class:`RegistrationProfile` with expired activation keys and
      with associated user accounts which are inactive (have their
      ``is_active`` field set to ``False``). To disable a user account
      without having it deleted, simply delete its associated
      :class:`RegistrationProfile`; any ``User`` which does not have
      an associated :class:`RegistrationProfile` will not be deleted.

      A custom management command is provided which will execute this
      method, suitable for use in cron jobs or other scheduled
      maintenance tasks: ``manage.py cleanupregistration``.

      :rtype: ``None``

   .. method:: create_inactive_user(username, email, password, site[, send_email])

      Creates a new, inactive user account and an associated instance
      of :class:`RegistrationProfile`, sends the activation email and
      returns the new ``User`` object representing the account.

      :param username: The username to use for the new account.
      :type username: string
      :param email: The email address to use for the new account.
      :type email: string
      :param password: The password to use for the new account.
      :type password: string
      :param site: An object representing the site on which the
         account is being registered.
      :type site: ``django.contrib.sites.models.Site`` or
         ``django.contrib.sites.models.RequestSite``
      :param send_email: If ``True``, the activation email will be
         sent to the account (by calling
         :meth:`RegistrationProfile.send_activation_email`). If
         ``False``, no email will be sent (but the account will still
         be inactive)
      :type send_email: bool
      :rtype: ``User``

   .. method:: create_profile(user)

      Creates and returns a :class:`RegistrationProfile` instance for
      the account represented by ``user``.

      The ``RegistrationProfile`` created by this method will have its
      :attr:`~RegistrationProfile.activation_key` set to a SHA1 hash
      generated from a combination of the account's username and a
      random salt.

      :param user: The user account; an instance of
         ``django.contrib.auth.models.User``.
      :type user: ``User``
      :rtype: ``RegistrationProfile``
