.. _faq:

Frequently-asked questions
==========================

The following are miscellaneous common questions and answers related
to installing/using django-registration, culled from bug reports,
emails and other sources.


Do I need to rewrite the views to change the way they behave?
-------------------------------------------------------------

No. There are several ways you can customize behavior without making
any changes whatsoever:

* Pass custom arguments -- e.g., to specify forms, template names,
  etc. -- to :ref:`the registration views <views>`.

* Use the :ref:`signals <signals>` sent by the views to add custom
  behavior.

* Write a custom :ref:`registration backend <backend-api>` which
  implements the behavior you need, and have the views use your
  backend.

If none of these are sufficient, your best option is likely to simply
write your own views; however, it is hoped that the level of
customization exposed by these options will be sufficient for nearly
all user-registration workflows.


How do I pass custom arguments to the views?
--------------------------------------------

Part 3 of the official Django tutorial, when it `introduces generic
views
<http://docs.djangoproject.com/en/dev/intro/tutorial04/#use-generic-views-less-code-is-better>`_,
covers the necessary mechanism: simply provide a dictionary of keyword
arguments in your URLconf.


Does that mean I should rewrite django-registration's default URLconf?
----------------------------------------------------------------------

No; if you'd like to pass custom arguments to the registration views,
simply write and include your own URLconf instead of including the
default one provided with django-registration.


I don't want to write my own URLconf because I don't want to write patterns for all the auth views!
---------------------------------------------------------------------------------------------------

You're in luck, then; django-registration provides a URLconf which
*only* contains the patterns for the auth views, and which you can
include in your own URLconf anywhere you'd like; it lives at
``registration.auth_urls``.


I don't like the names you've given to the URL patterns!
--------------------------------------------------------

In that case, you should feel free to set up your own URLconf which
uses the names you want.


How do I log a user in immediately after registration or activation?
--------------------------------------------------------------------

You can most likely do this simply by writing a function which listens
for the appropriate :ref:`signal <signals>`; your function should set
the ``backend`` attribute of the user to the correct authentication
backend, and then call ``django.contrib.auth.login()`` to log the user
in.
