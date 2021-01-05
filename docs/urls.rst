.. _urls:
.. module:: registration.urls

Registration urls
==================

If you do not wish to configure all of your own URLs for the various registration views, there are several default definitions that you can include in your ``urls.py`` file.

There is an URL file for :ref:`each of the default backends <basic-urls>`. These files provide all the URLs that you will need for normal interaction.

If you wish to include just the authentication URLs, either because you want to expose them under a different path, or because you want to manually configure the URLs for the other views, there is a separate :ref:`include for that <authentication-urls>`.

.. _basic-urls:

Basic URLs
~~~~~~~~~~

These URLs are provided by any of the following:
 * ``registration.backends.default.urls``
 * ``registration.backends.admin_approval.urls``
 * ``registration.backends.simple.urls``

**login/**
 * View: ``django.contrib.auth.views.LoginView``

**logout/**
 * View: ``django.contrib.auth.views.LogoutView``

**password/change/**
 * View: ``django.contrib.auth.views.PasswordChangeDoneView``

**password/change/done/**
 * View: ``django.contrib.auth.views.PasswordResetView``

**password/reset/**
 * View: ``django.contrib.auth.views.PasswordResetView``

**password/reset/complete/**
 * View: ``django.contrib.auth.views.PasswordResetCompleteView``

**password/reset/done/**
 * View: ``django.contrib.auth.views.PasswordResetDoneView``

**password/reset/confirm/{token}/**
 * View: ``django.contrib.auth.views.PasswordResetConfirmView``

**register/**
 * View: :py:class:`registration.views.RegistrationView`
 * Template: :ref:`registration_form.html`

**register/closed/**
 * Template: :ref:`registration_closed.html`

.. _authentication-urls:

Authentication URLs
~~~~~~~~~~~~~~~~~~~~

Provided by ``registration.auth_urls``, or any of the above includes.

**activate/complete/**
 * Template: :ref:`activation_complete.html`

**activate/resend/**
 * View: :py:class:`registration.views.ResendActivationView`
 * Template: :ref:`resend_activation_complete.html`

**activate/{key}/**
 * View: :py:class:`registration.views.ActivationView`
 * Template: :ref:`activate.html`

**register/complete/**
 * Template: :ref:`registration_complete.html`

Admin approval backend
~~~~~~~~~~~~~~~~~~~~~~

This URL is only provided by ``registration.backends.admin_approval.urls``.

**approve/{profile}/**
 * View: :py:class:`registration.backends.admin_approval.views.ApprovalView`
 * Template: ``registration/admin_approve.html``

