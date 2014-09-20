.. django-registration-redux documentation master file, created by
   sphinx-quickstart on Mon Jun 22 02:57:42 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

|project| |version| documentation
=================================

This documentation covers the |version| release of
|project|, a simple but extensible application providing
user registration functionality for `Django
<http://www.djangoproject.com>`_ powered websites.

Although nearly all aspects of the registration process are
customizable, out-of-the-box support is provided for two common use
cases:

* Two-phase registration, consisting of initial signup followed by a
  confirmation email with instructions for activating the new account.

* One-phase registration, where a user signs up and is immediately
  active and logged in.

To get up and running quickly, consult the :ref:`quick-start guide
<quickstart>`, which describes all the necessary steps to install
|project| and configure it for the default workflow. For
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
   default-backend
   simple-backend
   forms
   views
   signals
   faq

.. seealso::

   * `Django's authentication documentation
     <http://docs.djangoproject.com/en/dev/topics/auth/>`_; Django's
     authentication system is used by |project|'s default
     configuration.
