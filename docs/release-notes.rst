.. _release-notes:

Release notes
=============

The |version| release of django-registration represents a complete
rewrite of the previous codebase, and as such introduces a number of
new features and greatly enhances the flexibility and customizability
of django-registration. This document summarizes those features; for a
list of changes which impact existing installations, consult :ref:`the
upgrade guide <upgrade>`.


The backend system
------------------

The largest overall change consists of factoring out the logic of user
registration into pluggable/swappable backend classes. The
:ref:`registration views <views>` now accept a (required) argument,
``backend``, which indicates the backend class to use, and that class
has full control over the registration (and, if needed, activation)
process, including:

* Determining whether registration will be allowed at all, on a
  per-request basis.

* Specifying a form class to use for account registration.

* Implementing the actual process of account creation.

* Determining whether a separate activation step is needed, and if so
  what it will entail.

* Specifying actions to take (e.g., redirects, automatic login, etc.)
  following successful registration or activation.

For full details, see the documentation for :ref:`the backend API
<backend-api>`.

The workflow used by previous releases of django-registration
(two-step registration/activation) has been implemented using this
system, and is shipped as :ref:`the default backend <default-backend>`
in django-registration |version|.


Other new features
------------------

An alternate :ref:`one-step registration system <simple-backend>` is
provided, for use by sites which do not require a two-step
registration/activation system.

During the registration and (optional) activation process,
:ref:`custom signals <signals>` are now sent, allowing easy injection
of custom processing into the registration workflow without needing to
write a full backend.

The default backend now supplies several `custom admin actions
<http://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/>`_ to
make the process of administering a site with django-registration
simpler.

The :func:`~registration.views.activate` view now supplies any
captured keyword arguments from the URL (in the case of the default
backend, this is the activation key) to its template in case of
unsuccessful activation; this greatly simplifies the process of
determining why activation failed and displaying appropriate error
messages.

