.. django-registration documentation master file, created by
   sphinx-quickstart on Mon Jun 22 02:57:42 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-registration 0.8 documentation
=====================================

This documentation covers the 0.8 release of django-registration, a
simple but extensible application providing user registration
functionality for `Django <http://www.djangoproject.com>`_-powered
websites.

Although nearly all aspects of the registration process are
customizable, the default setup of django-registration attempts to
cover the most common use case: two-phase registration, consisting of
initial signup followed by a confirmation email which contains
instructions for activating the new account.

To get up and running quickly, consult the :ref:`quick-start guide
<quickstart>`, which describes all the necessary steps to install
django-registration and configure it for the default workflow. For
more detailed information, including how to customize the registration
process (and support for alternate registration systems), read through
the documentation listed below.

If you are upgrading from a previous release, please read the
:ref:`upgrade guide <upgrade>` for information on what's changed.

Contents:

.. toctree::
   :maxdepth: 1
   
   quickstart
   release-notes
   upgrade
   backend-api
   default-backend
   simple-backend
   forms
   views
   signals
   faq

.. seealso::

   * `Django's authentication documentation
     <http://docs.djangoproject.com/en/dev/topics/auth/>`_; Django's
     authentication system is used by django-registration's default
     configuration.

   * `django-profiles
     <http://bitbucket.org/ubernostrum/django-profiles/>`_, an
     application which provides simple user-profile management.
