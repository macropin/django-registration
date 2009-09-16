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
in 0.8 it raises a ``PendingDeprecationWarning`` (which is ignored by
default in Python), in 0.9 it will raise ``DeprecationWarning`` (which
will begin printing warning messages on import) and in 1.0 it will be
removed entirely.
