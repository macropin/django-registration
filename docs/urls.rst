.. _urls:
.. module:: registration.urls

Registration urls
==================

If you do not wish to configure all of your own URLs for the various registration views, there are several default definitions that you can include in your `urls.py` file.

Basic URLs
~~~~~~~~~~

These URLs are provided by any of the following:
 * ``registration.backends.default.urls``
 * ``registration.backends.admin_approval.urls``
 * ``registration.backends.simple.urls``

**login/**
 * View: `django.contrib.auth.views.LoginView`

**logout/**
 * View: `django.contrib.auth.views.LogoutView`

**password/change/**
 * View: `django.contrib.auth.views.PasswordChangeDoneView`

**password/change/done/**
 * View: `django.contrib.auth.views.PasswordResetView`

**password/reset/**
 * View: `django.contrib.auth.views.PasswordResetView`

**password/reset/complete/**
 * View: `django.contrib.auth.views.PasswordResetCompleteView`

**password/reset/done/**
 * View: `django.contrib.auth.views.PasswordResetDoneView`

**password/reset/confirm/{token}/**
 * View: `django.contrib.auth.views.PasswordResetConfirmView`

**register/**
 * View: :py:class:`registration.views.RegistrationView`
 * Template: :ref:`registration_form.html <registration/registration_form.html>`

**register/closed/**
 * Template: `registration/registration_closed.html`

Authentication views
~~~~~~~~~~~~~~~~~~~~

Provided by ``registration.auth_urls``, or any of the above includes.

**activate/complete/**
 * Template: :ref:`activation_complete.html <registration/activation_complete.html>`

**activate/resend/**
 * View: :py:class:`registration.views.ResendActivationView`
 * Template: `registration/resend_activation_complete.html`

**activate/{key}/**
 * View: :py:class:`registration.views.ActivationView`
 * Template: :ref:`activate.html <registration/activate.html>`

**register/complete/**
 * Template: :ref:`registration_complete.html <registration/registration_complete.html>`

**register/closed/**
 * Template: `registration/registration_closed.html`

Admin approval backend
~~~~~~~~~~~~~~~~~~~~~~

Provided by `registration.backends.admin_approval.urls`

**approve/{profile}/**
 * View: :py:class:`registration.backends.admin_approval.views.ApprovalView`
 * Template: `registration/admin_approve.html`

