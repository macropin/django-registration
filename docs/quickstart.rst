.. _quickstart:

Quick start guide
=================

Before installing |project|, you'll need to have a copy of
`Django <http://www.djangoproject.com>`_ already installed. For the
|version| release, Django 1.7 or newer is required.

For further information, consult the `Django download page
<http://www.djangoproject.com/download/>`_, which offers convenient
packaged downloads and installation instructions.


Installing |project|
--------------------

There are several ways to install |project|:

* Automatically, via a package manager.

* Manually, by downloading a copy of the release package and
  installing it yourself.

* Manually, by performing a Git checkout of the latest code.

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
the recommended one is `pip <https://pip.pypa.io/>`_.

Using ``pip``, type::

    pip install django-registration-redux

It is also possible that your operating system distributor provides a
packaged version of |project|. Consult your
operating system's package list for details, but be aware that
third-party distributions may be providing older versions of
|project|, and so you should consult the documentation which
comes with your operating system's package.


Manual installation from a downloaded package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer not to use an automated package installer, you can
download a copy of |project| and install it manually. The
latest release package can be downloaded from |project|'s
`listing on the Python Package Index
<http://pypi.python.org/pypi/django-registration-redux/>`_.

Once you've downloaded the package, unpack it (on most operating
systems, simply double-click; alternately, type ``tar zxvf
django-registration-redux-1.1.tar.gz`` at a command line on Linux, Mac OS X
or other Unix-like systems). This will create the directory
``django-registration-redux-1.1``, which contains the ``setup.py``
installation script. From a command line in that directory, type::

    python setup.py install

Note that on some systems you may need to execute this with
administrative privileges (e.g., ``sudo python setup.py install``).


Manual installation from a Git checkout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you'd like to try out the latest in-development code, you can
obtain it from the |project| repository, which is hosted at
`Github <http://github.com/>`_ and uses `Git
<http://git-scm.com/>`_ for version control. To
obtain the latest code and documentation, you'll need to have
Git installed, at which point you can type::

    git clone https://github.com/macropin/django-registration.git

You can also obtain a copy of a particular release of
|project| by specifying the ``-b`` argument to ``git clone``;
each release is given a tag of the form ``vX.Y``, where "X.Y" is the
release number. So, for example, to check out a copy of the |version|
release, type::

    git clone -b v1.0 https://github.com/macropin/django-registration.git

In either case, this will create a copy of the |project|
Git repository on your computer; you can then add the
``django-registration-redux`` directory inside the checkout your Python
import path, or use the ``setup.py`` script to install as a package.


Basic configuration and use
---------------------------

Once installed, you can add |project| to any Django-based
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


Settings
~~~~~~~~

Begin by adding ``registration`` to the ``INSTALLED_APPS`` setting of
your project, and specifying one additional setting:

``ACCOUNT_ACTIVATION_DAYS``
    This is the number of days users will have to activate their
    accounts after registering. If a user does not activate within
    that period, the account will remain permanently inactive and may
    be deleted by maintenance scripts provided in |project|.

``REGISTRATION_DEFAULT_FROM_EMAIL``
    Optional. If set, emails sent through the registration app will use this
    string. Falls back to using Django's built-in ``DEFAULT_FROM_EMAIL``
    setting.

``REGISTRATION_EMAIL_HTML``
    Optional. If this is `False`, registration emails will be send in plain
    text. If this is `True`, emails will be sent as HTML. Defaults to `True`.

``REGISTRATION_AUTO_LOGIN``
    Optional. If this is `True`, your users will automatically log in when they
    click on the activation link in their email. Defaults to `False`.

For example, you might have something like the following in your
Django settings file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sites',
        'registration',
        # ...other installed applications...
    )

    ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
    REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.

Once you've done this, run ``python manage.py migrate`` to install the model
used by the default setup.


Setting up URLs
~~~~~~~~~~~~~~~

The :ref:`default backend <default-backend>` includes a Django
``URLconf`` which sets up URL patterns for :ref:`the views in
django-registration-redux <views>`, as well as several useful views in
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


Templates
~~~~~~~~~

The templates in |project| assume you have a `base.html` template in your
project's template directory. This base template should include a ``title`` block and a ``content`` block. Other than that, every template needed is
included.  You can extend and customize the included templates as needed. Some
of the templates you'll probably want to customize are covered here:

Note that, with the exception of the templates used for account activation
emails, all of these are rendered using a ``RequestContext`` and so will also
receive any additional variables provided by `context processors
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

**IMPORTANT**: If you override this template, you must also override the HTML
version (below), or disable HTML emails by adding
``REGISTRATION_EMAIL_HTML = False`` to your settings.py.

Used to generate the text body of the activation email. Should display a
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

``user``
    The new user account

**registration/activation_email.html**

This template is used to generate the html body of the activation email.
Should display the same content as the text version of the activation email.

The context available is the same as the text version of the template.
