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


Django version requirement
--------------------------

As of |version|, django-registration requires Django 1.3 or newer;
older Django releases may work, but are officially unsupported.


Backwards-incompatible changes
------------------------------

If you're upgrading from an older release of django-registration, and
if you were using the default setup (i.e., the included default
URLconf and no custom URL patterns or custom arguments to views), most
things will continue to work as normal (although you will need to
create one new template; see the section on views below). However, the
old default URLconf has been deprecated and will be removed in version
1.0 of django-registration, so it is recommended that you begin
migrating now. To do so, change any use of ``registration.urls`` to
``registration.backends.default.urls``. For example, if you had the
following in your root URLconf::

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

:ref:`The views used to handle user registration <views>` have changed
significantly as of django-registration |version|. Both views now
require the keyword argument ``backend``, which specifies the
:ref:`registration backend <backend-api>` to use, and so any URL
pattern for these views must supply that argument. The URLconf
provided with :ref:`the default backend <default-backend>` properly
passes this argument.

The ``profile_callback`` argument of the
:func:`~registration.views.register` view has been removed; the
functionality it provided can now be implemented easily via a custom
backend, or by connecting listeners to :ref:`the signals sent during
the registration process <signals>`.

The :func:`~registration.views.activate` view now issues a redirect
upon successful activation; in the default backend this is to the URL
pattern named ``registration_activation_complete``; in the default
setup, this will redirect to a view which renders the template
``registration/activation_complete.html``, and so this template should
be present when using the default backend and default
configuration. Other backends can specify the location to redirect to
through their ``post_activation_redirect()`` method, and this can be
overridden on a case-by-case basis by passing the (new) keyword
argument ``success_url`` to the ``activate()`` view. On unsuccessful
activation, the ``activate()`` view still displays the same template,
but its context has changed: the context will simply consist of any
keyword arguments captured in the URL and passed to the view.


Changes to registration forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previously, the form used to collect data during registration was
expected to implement a ``save()`` method which would create the new
user account. This is no longer the case; creating the account is
handled by the backend, and so any custom logic should be moved into a
custom backend, or by connecting listeners to :ref:`the signals sent
during the registration process <signals>`.


Changes to the :class:`~registration.models.RegistrationProfile` model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The
:meth:`~registration.models.RegistrationManager.create_inactive_user`
method of :class:`~registration.models.RegistrationManager` now has an
additional required argument: ``site``. This allows
django-registration to easily be used regardless of whether
``django.contrib.sites`` is installed, since a ``RequestSite`` object
can be passed in place of a regular ``Site`` object.

The :data:`~registration.signals.user_registered` signal is no longer
sent by ``create_inactive_user()``, and the
:data:`~registration.signals.user_activated` signal is no longer sent
by :meth:`~registration.models.RegistrationManager.activate_user`;
these signals are now sent by the backend after these methods have
been called. Note that :ref:`these signals <signals>` were added after
the django-registration 0.7 release but before the refactoring which
introduced :ref:`the backend API <backend-api>`, so only installations
which were tracking the in-development codebase will have made use of
them.

The sending of activation emails has been factored out of
``create_inactive_user()``, and now exists as the method
:meth:`~registration.models.RegistrationProfile.send_activation_email`
on instances of ``RegistrationProfile``.
