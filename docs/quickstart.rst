.. _quickstart:

Quick start guide
=================

Before installing django-registration, you'll need to have a copy of
`Django <http://www.djangoproject.com>`_ already installed. For the
|version| release, Django 1.4 or newer is required.

For further information, consult the `Django download page
<http://www.djangoproject.com/download/>`_, which offers convenient
packaged downloads and installation instructions.


Installing django-registration
------------------------------

There are several ways to install django-registration:

* Automatically, via a package manager.

* Manually, by downloading a copy of the release package and
  installing it yourself.

* Manually, by performing a Mercurial checkout of the latest code.

It is also highly recommended that you learn to use `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ for development and
deployment of Python software; ``virtualenv`` provides isolated Python
environments into which collections of software (e.g., a copy of
Django, and the necessary settings and applications for deploying a
site) can be installed, without conflicting with other installed
software. This makes installation, testing, management and deployment
far simpler than traditional site-wide installation of Python
packages.


Automatic installation via a package manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several automatic package-installation tools are available for Python;
the recommended one is `pip <http://pip.openplans.org/>`_.

Using ``pip``, type::

    pip install django-registration

It is also possible that your operating system distributor provides a
packaged version of django-registration (for example, `Debian
GNU/Linux <http://debian.org/>`_ provides a package, installable via
``apt-get-install python-django-registration``). Consult your
operating system's package list for details, but be aware that
third-party distributions may be providing older versions of
django-registration, and so you should consult the documentation which
comes with your operating system's package.


Manual installation from a downloaded package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer not to use an automated package installer, you can
download a copy of django-registration and install it manually. The
latest release package can be downloaded from `django-registration's
listing on the Python Package Index
<http://pypi.python.org/pypi/django-registration/>`_.

Once you've downloaded the package, unpack it (on most operating
systems, simply double-click; alternately, type ``tar zxvf
django-registration-0.9.tar.gz`` at a command line on Linux, Mac OS X
or other Unix-like systems). This will create the directory
``django-registration-0.9``, which contains the ``setup.py``
installation script. From a command line in that directory, type::

    python setup.py install

Note that on some systems you may need to execute this with
administrative privileges (e.g., ``sudo python setup.py install``).


Manual installation from a Mercurial checkout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you'd like to try out the latest in-development code, you can
obtain it from the django-registration repository, which is hosted at
`Bitbucket <http://bitbucket.org/>`_ and uses `Mercurial
<http://www.selenic.com/mercurial/wiki/>`_ for version control. To
obtain the latest code and documentation, you'll need to have
Mercurial installed, at which point you can type::

    hg clone http://bitbucket.org/ubernostrum/django-registration/

You can also obtain a copy of a particular release of
django-registration by specifying the ``-r`` argument to ``hg clone``;
each release is given a tag of the form ``vX.Y``, where "X.Y" is the
release number. So, for example, to check out a copy of the |version|
release, type::

    hg clone -r v|version| http://bitbucket.org/ubernostrum/django-registration/

In either case, this will create a copy of the django-registration
Mercurial repository on your computer; you can then add the
``django-registration`` directory inside the checkout your Python
import path, or use the ``setup.py`` script to install as a package.


Basic configuration and use
---------------------------

Once installed, you can add django-registration to any Django-based
project you're developing. The default setup will enable user
registration with the following workflow:

1. A user signs up for an account by supplying a username, email
   address and password.

2. From this information, a new ``User`` object is created, with its
   ``is_active`` field set to ``False``. Additionally, an activation
   key is generated and stored, and an email is sent to the user
   containing a link to click to activate the account.

3. Upon clicking the activation link, the new account is made active
   (the ``is_active`` field is set to ``True``); after this, the user
   can log in.

Note that the default workflow requires ``django.contrib.auth`` to be
installed, and it is recommended that ``django.contrib.sites`` be
installed as well. You will also need to have a working mail server
(for sending activation emails), and provide Django with the necessary
settings to make use of this mail server (consult `Django's
email-sending documentation
<http://docs.djangoproject.com/en/dev/topics/email/>`_ for details).


Required settings
~~~~~~~~~~~~~~~~~

Begin by adding ``registration`` to the ``INSTALLED_APPS`` setting of
your project, and specifying one additional setting:

``ACCOUNT_ACTIVATION_DAYS``
    This is the number of days users will have to activate their
    accounts after registering. If a user does not activate within
    that period, the account will remain permanently inactive and may
    be deleted by maintenance scripts provided in django-registration.

For example, you might have something like the following in your
Django settings file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sites',
        'registration',
        # ...other installed applications...
    )
    
    ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.

Once you've done this, run ``manage.py syncdb`` to install the model
used by the default setup.


Setting up URLs
~~~~~~~~~~~~~~~

The :ref:`default backend <default-backend>` includes a Django
``URLconf`` which sets up URL patterns for :ref:`the views in
django-registration <views>`, as well as several useful views in
``django.contrib.auth`` (e.g., login, logout, password
change/reset). This ``URLconf`` can be found at
``registration.backends.default.urls``, and so can simply be included
in your project's root URL configuration. For example, to place the
URLs under the prefix ``/accounts/``, you could add the following to
your project's root ``URLconf``::

    (r'^accounts/', include('registration.backends.default.urls')),

Users would then be able to register by visiting the URL
``/accounts/register/``, login (once activated) at
``/accounts/login/``, etc.

Another ``URLConf`` is also provided -- at ``registration.auth_urls``
-- which just handles the Django auth views, should you want to put
those at a different location.


Required templates
~~~~~~~~~~~~~~~~~~

In the default setup, you will need to create several templates
required by django-registration, and possibly additional templates
required by views in ``django.contrib.auth``. The templates requires
by django-registration are as follows; note that, with the exception
of the templates used for account activation emails, all of these are
rendered using a ``RequestContext`` and so will also receive any
additional variables provided by `context processors
<http://docs.djangoproject.com/en/dev/ref/templates/api/#id1>`_.

**registration/registration_form.html**

Used to show the form users will fill out to register. By default, has
the following context:

``form``
    The registration form. This will be an instance of some subclass
    of ``django.forms.Form``; consult `Django's forms documentation
    <http://docs.djangoproject.com/en/dev/topics/forms/>`_ for
    information on how to display this in a template.

**registration/registration_complete.html**

Used after successful completion of the registration form. This
template has no context variables of its own, and should simply inform
the user that an email containing account-activation information has
been sent.

**registration/activate.html**

Used if account activation fails. With the default setup, has the following context:

``activation_key``
    The activation key used during the activation attempt.

**registration/activation_complete.html**

Used after successful account activation. This template has no context
variables of its own, and should simply inform the user that their
account is now active.

**registration/activation_email_subject.txt**

Used to generate the subject line of the activation email. Because the
subject line of an email must be a single line of text, any output
from this template will be forcibly condensed to a single line before
being used. This template has the following context:

``activation_key``
    The activation key for the new account.

``expiration_days``
    The number of days remaining during which the account may be
    activated.

``site``
    An object representing the site on which the user registered;
    depending on whether ``django.contrib.sites`` is installed, this
    may be an instance of either ``django.contrib.sites.models.Site``
    (if the sites application is installed) or
    ``django.contrib.sites.models.RequestSite`` (if not). Consult `the
    documentation for the Django sites framework
    <http://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ for
    details regarding these objects' interfaces.

**registration/activation_email.txt**

Used to generate the body of the activation email. Should display a
link the user can click to activate the account. This template has the
following context:

``activation_key``
    The activation key for the new account.

``expiration_days``
    The number of days remaining during which the account may be
    activated.

``site``
    An object representing the site on which the user registered;
    depending on whether ``django.contrib.sites`` is installed, this
    may be an instance of either ``django.contrib.sites.models.Site``
    (if the sites application is installed) or
    ``django.contrib.sites.models.RequestSite`` (if not). Consult `the
    documentation for the Django sites framework
    <http://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ for
    details regarding these objects' interfaces.

Note that the templates used to generate the account activation email
use the extension ``.txt``, not ``.html``. Due to widespread antipathy
toward and interoperability problems with HTML email,
django-registration defaults to plain-text email, and so these
templates should simply output plain text rather than HTML.

To make use of the views from ``django.contrib.auth`` (which are set
up for you by the default URLconf mentioned above), you will also need
to create the templates required by those views. Consult `the
documentation for Django's authentication system
<http://docs.djangoproject.com/en/dev/topics/auth/>`_ for details
regarding these templates.
