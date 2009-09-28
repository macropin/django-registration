.. _upgrade:

Upgrade guide
=============

The |version| release of django-registration represents a complete
rewrite of the previous codebase, and introduces several new features
which greatly enhance the customizability and extensibility of
django-registration. Whenever possible, changes were made in ways
which preserve backwards compatibility with previous releases, but
some changes to existing installations will still be required in order
to upgrade to |version|. This document provides a summary of those
changes, and of the new features available in the |version| release.


Backwards-incompatible changes
------------------------------

If you're upgrading from an older release of django-registration, and
if you were using the default setup (i.e., the included default
URLConf and no custom URL patterns or custom arguments to views), you
will not need to make any immediate changes. However, the old default
URLConf has been deprecated and will be removed in version 1.0 of
django-registration, so it is recommended that you begin migrating
now. To do so, change any use of ``registration.urls`` to
``registration.backends.default.urls``. For example, if you had the
following in your root URLConf::

    (r'^accounts/', include('registration.urls')),

you should change it to::

    (r'^accounts/', include('registration.backends.default.urls')),

The older include will continue to work until django-registration 1.0;
in |version| it raises a ``PendingDeprecationWarning`` (which is
ignored by default in Python), in 0.9 it will raise
``DeprecationWarning`` (which will begin printing warning messages on
import) and in 1.0 it will be removed entirely.

Changes to registration views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The views used to handle user registration have changed significantly
as of django-registration |version|. Both views now require the
keyword argument ``backend``, which specifies the :ref:`registration
backend <backend-api>` to use, and so any URL pattern for these views
must supply that argument.

The ``profile_callback`` argument of the ``register`` view has been
removed; the functionality it provided can now be implemented easily
via a custom backend, or by connecting listeners to :ref:`the signals
sent during the registration process <signals>`.

Changes to registration forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previously, the form used to collect data during registration was
expected to implement a ``save()`` method which would create the new
user account. This is no longer the case; creating the account is
handled by the backend, and so any custom logic should be moved into a
custom backend, or by connecting listeners to :ref:`the signals sent
during the registration process <signals>`.

Changes to the ``RegistrationProfile`` model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``RegistrationProfile.objects.create_inactive_user()`` now
has an additional required argument: ``site``. This allows
django-registration to easily be used regardless of whether
``django.contrib.sites`` is installed, since a ``RequestSite`` object
can be passed in place of a regular ``Site`` object.

The :data:`~registration.signals.user_registered` signal is no longer
sent by ``RegistrationProfile.objects.create_inactive_user()``, and
the :data:`~registration.signals.user_activated` signal is no longer
sent by ``RegistrationProfile.objects.activate_user()``; these signals
are now sent by the backend after these methods have been called.

The sending of activation emails has been factored out of
``RegistrationProfile.objects.create_inactive_user()``, and now exists
as the method ``send_activation_email()`` on instances of
``RegistrationProfile``.
