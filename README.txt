===================
Django Registration
===================

This is a fairly simple user-registration application for Django_,
designed to make allowing user signups as painless as possible. It
requires a recent Subversion checkout of Django, since it uses
newforms and a couple other post-0.95 additions. Aside from that, it
has no external dependencies.


Installation notes
==================

Google Code recommends doing the Subversion checkout like so::

    svn checkout http://django-registration.googlecode.com/svn/trunk/ django-registration

But the hyphen in the application name can cause issues installing
into a DB, so it's really better to do this::

    svn checkout http://django-registration.googlecode.com/svn/trunk/ registration

If you've already downloaded, rename the directory before installing.

Then just add ``registration`` to the ``INSTALLED_APPS`` setting of
your project, and you should be good to go.

Note that one of the templates included with this app uses the
``humanize`` library, so you'll want to have
``django.contrib.humanize`` installed if you don't already.


The short and sweet instructions
================================

Here's the workflow for user signup:

1. User signs up for account.
2. User gets emailed an activation link.
3. User clicks the activation link before it expires.
4. User becomes a happy and productive contributor to your site.

To make this work, start by putting this app into your
``INSTALLED_APPS`` setting and running ``syncdb``. Then, add a new
setting in your settings file: ``ACCOUNT_ACTIVATION_DAYS``. This
should be a number, and will be used as the number of days before an
activation key expires.

Finally, drop this line into your root URLConf::

    (r'^accounts/', include('registration.urls')),

And point people at the URL ``/accounts/register/``. Things should
Just Work.


If emails never get sent
========================

Welcome to the world of spam filtering! Assuming your server settings
are correct and Django is otherwise able to send email, the most
likely problem is overzealous filtering on the receiving end. Many
spam filtering solutions are depressingly overactive and love to eat
account-registration emails.

If you know how to solve this, you will make millions of dollars.


How it works under the hood
===========================

This app defines one model -- ``RegistrationProfile`` -- which is tied
to the ``User`` model via a unique foreign key (so there can only ever
be one ``RegistrationProfile`` per ``User``), and which stores an
activation key and the date/time the key was generated.

There's a custom manager on ``RegistrationProfile`` which has two
important methods:

1. ``create_inactive_user`` takes a username, email address and
   password, and first creates a new ``User``, setting the
   ``is_active`` field to ``False``. Then it generates an activation
   key and creates a ``RegistrationProfile`` for that
   ``User``. Finally, it sends an email to the new user with an
   activation link to click on.
2. ``activate_user`` takes an activation key, looks up the
   ``RegistrationProfile`` it goes with, and sets ``is_active`` to
   ``True`` on the corresponding ``User``.

The views and form defined in this app basically exist solely to
expose this functionality over the Web. The registration form, used in
the initial sign-up view, does a little checking to make sure that the
username isn't taken and that the user types a password twice without
typos, but once that validation is taken care of everything gets
handed off to ``RegistrationProfile.objects.create_inactive_user``.

Similarly, the activation view doesn't do a whole lot other than call
``RegistrationProfile.objects.activate_user``.


Clearing out inactive accounts
==============================

Since activation keys do eventually expire (after however many days
you've specified in the ``ACCOUNT_ACTIVATION_DAYS`` setting), there's
a possibility that you'll end up with people who signed up but never
activated their accounts. And that's bad, because it clutters up your
database and it keeps the username they signed up with from ever
actually being used.

So there's also a third method defined on ``RegistrationProfile``'s
custom manager: ``delete_expired_users``. All it does is loop through
the DB, looking for inactive accounts with expired activation keys,
and deletes them. It's recommended that you run it every once in a
while (ideally, just set up a cron job to do it periodically) so you
can clear out any inactive accounts and free up those usernames.

The only time this isn't desirable is when you use the ``is_active``
field as a way to keep troublesome users under control -- when you set
``is_active`` to ``False``, they can't log in, which is pretty
handy. But that means you _want_ to have an inactive account in your
DB and you *don't* want ``delete_expired_users`` to delete it -- if
that happened, the troublemaker could just re-create the account and
start all over again.

For this reason, ``delete_expired_users`` looks first at the
``RegistrationProfile`` table, and only goes into the ``User`` table
when it finds expired profiles. So to keep a ``User`` around and
permanently inactive, just manually delete their
``RegistrationProfile`` instance and ``delete_inactive_users`` will
never touch their account.


A note on templates
===================

I've included examples of all the templates this app expects, bundled
into the ``templates`` directory; so long as you have the "app
directories" template loader
(``django.template.loaders.app_directories.load_template_source``) in
your ``TEMPLATE_LOADERS`` setting (and it's in there by default), you
should be able to just edit them in-place to suit your site's layout,
and Django will pick them up automatically.

The included template for activation emails requires the ``humanize``
library, so if you use it as-is, be sure to add
``django.contrib.humanize`` to your ``INSTALLED_APPS`` setting.

Questions? Problems?
====================

If you've got a question that isn't covered here or in the comments
and docstrings in the code, or if you run into a bug, swing on over to
`this app's Google Code project page`_ and file a new "issue". I'll do
my best to respond promptly.


.. _Django: http://www.djangoproject.com/
.. _this app's Google Code project page: http://code.google.com/p/django-registration/
 