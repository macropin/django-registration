.. _signals:
.. module:: registration.signals


Custom signals used by django-registration
==========================================

Much of django-registration's customizability comes through the
ability to write and use :ref:`registration backends <backend-api>`
implementing different workflows for user registration. However, there
are many cases where only a small bit of additional logic needs to be
injected into the registration process, and writing a custom backend
to support this represents an unnecessary amount of work. A more
lightweight customization option is provided through two custom
signals which backends are required to send at specific points during
the registration process; functions listening for these signals can
then add whatever logic is needed.

For general documentation on signals and the Django dispatcher,
consult `Django's signals documentation
<http://docs.djangoproject.com/en/dev/topics/signals/>`_. This
documentation assumes that you are familiar with how signals work and
the process of writing and connecting functions which will listen for
signals.


.. data:: user_activated

   Sent when a user account is activated (not applicable to all
   backends). Provides the following arguments:

   ``sender``
       The backend class used to activate the user.

   ``user``
        An instance of ``django.contrib.auth.models.User``
        representing the activated account.

   ``request``
       The ``HttpRequest`` in which the account was activated.


.. data:: user_registered

   Sent when a new user account is registered. Provides the following
   arguments:

   ``sender``
       The backend class used to register the account.

   ``user``
        An instance of ``django.contrib.auth.models.User``
        representing the new account.

   ``request``
        The ``HttpRequest`` in which the new account was registered.
