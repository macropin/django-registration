.. _faq:

Frequently-asked questions
==========================

The following are miscellaneous common questions and answers related
to installing/using django-registration, culled from bug reports,
emails and other sources.


General
-------

**What license is django-registration under?**
    django-registration is offered under a three-clause BSD-style
    license; this is `an OSI-approved open-source license
    <http://www.opensource.org/licenses/bsd-license.php>`_, and allows
    you a large degree of freedom in modifiying and redistributing the
    code. For the full terms, see the file ``LICENSE`` which came with
    your copy of django-registration; if you did not receive a copy of
    this file, you can view it online at
    <http://bitbucket.org/ubernostrum/django-registration/src/tip/LICENSE>.

**Why are the forms and models for the default backend not in the default backend?**
    The model and manager used by :ref:`the default backend
    <default-backend>` are in ``registration.models``, and the default
    form class (and various subclasses) are in ``registration.forms``;
    logically, they might be expected to exist in
    ``registration.backends.default``, but there are several reasons
    why that's not such a good idea:

    1. Older versions of django-registration made use of the model and
       form classes, and moving them would create an unnecessary
       backwards incompatibility: ``import`` statements would need to
       be changed, and some database updates would be needed to
       reflect the new location of the
       :class:`~registration.models.RegistrationProfile` model.

    2. Due to the design of Django's ORM, the ``RegistrationProfile``
       model would end up with an ``app_label`` of ``default``, which
       isn't particularly descriptive and may conflict with other
       applications. By keeping it in ``registration.models``, it
       retains an ``app_label`` of ``registration``, which more
       accurately reflects what it does and is less likely to cause
       problems.

    3. Although the ``RegistrationProfile`` model and the various
       :ref:`form classes <forms>` are used by the default backend,
       they can and are meant to be reused as needed by other
       backends. Any backend which uses an activation step should feel
       free to reuse the ``RegistrationProfile`` model, for example,
       and the registration form classes are in no way tied to a
       specific backend (and cover a number of common use cases which
       will crop up regardless of the specific backend logic in use).


Installation and setup
----------------------

**How do I install django-registration?**
    Full instructions are available in :ref:`the quick start guide <quickstart>`.

**Do I need to put a copy of django-registration in every project I use it in?**
    No; putting applications in your project directory is a very bad
    habit, and you should stop doing it. If you followed the
    instructions mentioned above, django-registration was installed
    into a location that's on your Python import path, so you'll only
    ever need to add ``registration`` to your ``INSTALLED_APPS``
    setting (in any project, or in any number of projects), and it
    will work.

**Does django-registration come with any sample templates I can use right away?**
    No, for two reasons:

    1. Providing default templates with an application is generally
       hard to impossible, because different sites can have such
       wildly different design and template structure. Any attempt to
       provide templates which would work with all the possibilities
       would probably end up working with none of them.

    2. A number of things in django-registration depend on the
       specific :ref:`registration backend <backend-api>` you use,
       including the variables which end up in template
       contexts. Since django-registration has no way of knowing in
       advance what backend you're going to be using, it also has no
       way of knowing what your templates will need to look like.
    
    Fortunately, however, django-registration has good documentation
    which explains what context variables will be available to
    templates, and so it should be easy for anyone who knows Django's
    template system to create templates which integrate with their own
    site.


Configuration
-------------

**Do I need to rewrite the views to change the way they behave?**

    Not always. Any behavior controlled by an attribute on a
    class-based view can be changed by passing a different value for
    that attribute in the URLConf. See `Django's class-based view
    documentation
    <https://docs.djangoproject.com/en/1.5/topics/class-based-views/#simple-usage-in-your-urlconf>`_
    for examples of this.

    For more complex or fine-grained control, you will likely want to
    subclass :class:`~registration.views.RegistrationView` or
    :class:`~registration.views.ActivationView`, or both, add your
    custom logic to your subclasses, and then create a URLConf which
    makes use of your subclasses.
    
**I don't want to write my own URLconf because I don't want to write patterns for all the auth views!**
    You're in luck, then; django-registration provides a URLconf which
    *only* contains the patterns for the auth views, and which you can
    include in your own URLconf anywhere you'd like; it lives at
    ``registration.auth_urls``.

**I don't like the names you've given to the URL patterns!**
    In that case, you should feel free to set up your own URLconf
    which uses the names you want.

**I'm using Django 1.5 and a custom user model; how do I make that work?**
    Although the two built-in backends supplied with
    django-registration both assume Django's default ``User`` model,
    :ref:`the base view classes <views>` are deliberately
    user-model-agnostic. Simply subclass them, and implement logic for
    your custom user model.


Troubleshooting
---------------

**I've got functions listening for the registration/activation signals, but they're not getting called!**

    The most common cause of this is placing django-registration in a
    sub-directory that's on your Python import path, rather than
    installing it directly onto the import path as normal. Importing
    from django-registration in that case can cause various issues,
    including incorrectly connecting signal handlers. For example, if
    you were to place django-registration inside a directory named
    ``django_apps``, and refer to it in that manner, you would end up
    with a situation where your code does this::

        from django_apps.registration.signals import user_registered

    But django-registration will be doing::

        from registration.signals import user_registered

    From Python's point of view, these import statements refer to two
    different objects in two different modules, and so signal handlers
    connected to the signal from the first import will not be called
    when the signal is sent using the second import.

    To avoid this problem, follow the standard practice of installing
    django-registration directly on your import path and always
    referring to it by its own module name: ``registration`` (and in
    general, it is always a good idea to follow normal Python
    practices for installing and using Django applications).


Tips and tricks
---------------

**How do I log a user in immediately after registration or activation?**
    Take a look at the implementation of :ref:`the simple backend
    <simple-backend>`, which logs a user in immediately after
    registration.


**How do I re-send an activation email?**
    Assuming you're using :ref:`the default backend
    <default-backend>`, a `custom admin action
    <http://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/>`_
    is provided for this; in the admin for the
    :class:`~registration.models.RegistrationProfile` model, simply
    click the checkbox for the user(s) you'd like to re-send the email
    for, then select the "Re-send activation emails" action.

**How do I manually activate a user?**
    In the default backend, a custom admin action is provided for
    this. In the admin for the ``RegistrationProfile`` model, click
    the checkbox for the user(s) you'd like to activate, then select
    the "Activate users" action.