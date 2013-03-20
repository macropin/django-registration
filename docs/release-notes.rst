.. _release-notes:

Release notes
=============

The |version| release of django-registration represents a complete
rewrite of the previous codebase. For information on upgrading,
consult :ref:`the upgrade guide <upgrade>`.


The backend system
------------------

The largest overall change is that in place of the monolithic backend
classes and function-based views found in django-registration 0.8, in
|version| all views are class-based. A "backend" now consists of,
typically, one or two subclasses of :ref:`the built-in base views
<views>`.

Implementing these as class-based views allows for far simpler
configuration and customization, without the overhead involved in
supporting large numbers of optional keyword arguments to
function-based views, or the need to provide a separate class-based
infrastructure for implementing the logic of registration.

Notably, this implementation is also completely backwards-compatible
for users of django-registration 0.8 who simply used the recommended
default URLConf for one of the supplied backends; those URLConfs exist
in the same locations, and have been rewritten to point to the
appropriate class-based views with the appropriate options.