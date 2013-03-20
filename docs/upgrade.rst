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

As of |version|, django-registration requires Django 1.4 or newer;
older Django releases may work, but are officially unsupported.


Backwards-incompatible changes
------------------------------

If you're upgrading from an older release of django-registration, and
if you were using the default setup (i.e., the included default
URLconf and no custom URL patterns or custom arguments to views), you
do not need to make any chances.

If you had customized django-registration by writing your own backend,
you will now need to implement that backend by subclassing :ref:`the
built-in views <views>` and overriding or implementing your
customizations appropriately. Much of this is similar to previous
backend class implementations, so minimal changes to existing code
should be required.