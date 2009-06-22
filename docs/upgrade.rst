.. _upgrade:

Upgrade guide
=============

The 0.8 release of django-registration represents a complete rewrite
of the previous codebase, and introduces several new features which
greatly enhance the customizability and extensibility of
django-registration. Whenever possible, changes were made in ways
which preserve backwards compatibility with previous releases, but
some changes to existing installations will still be required in order
to upgrade to 0.8. This document provides a summary of those changes,
and of the new features available in the 0.8 release.


Backwards-incompatible changes
------------------------------

To upgrade from a previous version of django-registration, you will
need to make two changes, both to project configuration.

First, add the setting ``REGISTRATION_BACKEND``, and set it to
``"registration.backends.default.DefaultBackend"``. This is required
to support the primary new feature in 0.8 (pluggable backends
implementing different registration schemes), and will enable a
backend which provides behavior identical to previous releases of
django-registration.

Then, if you were using the default ``URLConf`` provided in previous
versions, you will instead need to use the ``URLConf`` provided by the
default backend in 0.8, which is located at
``registration.backends.default.urls``. So, for example, if you
previously had this in your ``URLConf``::

    (r'^accounts/', include('registration.urls')),

you will need to change it to::

    (r'^accounts/', include('registration.backends.default.urls')),
