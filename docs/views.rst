.. _views:
.. module:: registration.views

Registration views
==================

In order to allow the utmost flexibility in customizing and supporting
different workflows, django-registration makes use of Django's support
for `class-based views
<https://docs.djangoproject.com/en/dev/topics/class-based-views/>`_. Included
in django-registration are two base classes which can be subclassed to
implement whatever workflow is required.

.. class:: RegistrationView

   A subclass of Django's `FormView
   <https://docs.djangoproject.com/en/1.5/ref/class-based-views/generic-editing/#formview>`_,
   which provides the infrastructure for supporting user registration.

   Since it's a subclass of ``FormView``, ``RegistrationView`` has all
   the usual attributes and methods you can override; however, there
   is one key difference. In order to support additional
   customization, ``RegistrationView`` also passes the ``HttpRequest``
   to most of its methods. Subclasses do need to take this into
   account, and accept the ``request`` argument.

   Useful places to override or customize on a ``RegistrationView``
   subclass are:

   .. attribute:: disallowed_url

      The URL to redirect to when registration is disallowed. Should
      be a string, `the name of a URL pattern
      <https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns>`_. Default
      value is ``registration_disallowed``.

   .. attribute:: form_class

      The form class to use for user registration. Can be overridden
      on a per-request basis (see below). Should be the actual class
      object; by default, this class is
      :class:`registration.forms.RegistrationForm`.

   .. attribute:: success_url

      The URL to redirect to after successful registration. Should be
      a string, the name of a URL pattern, or a 3-tuple of arguments
      suitable for passing to Django's `redirect shortcut
      <https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#redirect>`. Can
      be overridden on a per-request basis (see below). Default value
      is ``None``, so that per-request customization is used instead.

   .. attribute:: template_name

      The template to use for user registration. Should be a
      string. Default value is
      ``registration/registration_form.html``.

   .. method:: get_form_class(request)

      Select a form class to use on a per-request basis. If not
      overridden, will use :attr:`~form_class`. Should be the actual
      class object.

   .. method:: get_success_url(request, user)

      Return a URL to redirect to after successful registration, on a
      per-request or per-user basis. If not overridden, will use
      :attr:`~success_url`. Should be a string, the name of a URL
      pattern, or a 3-tuple of arguments suitable for passing to
      Django's ``redirect`` shortcut.

   .. method:: registration_allowed(request)

      Should return a boolean indicating whether user registration is
      allowed, either in general or for this specific request.

   .. method:: register(request, **cleaned_data)

      Actually perform the business of registering a new
      user. Receives both the ``HttpRequest`` object and all of the
      ``cleaned_data`` from the registration form. Should return the
      new user who was just registered.


.. class:: ActivationView

   A subclass of Django's `TemplateView
   <https://docs.djangoproject.com/en/1.5/ref/class-based-views/base/#templateview>`_
   which provides support for a separate account-activation step, in
   workflows which require that.

   Useful places to override or customize on an ``ActivationView``
   subclass are:

   .. attribute:: template_name

      The template to use for user activation. Should be a
      string. Default value is ``registration/activate.html``.

   .. method:: activate(request, *args, **kwargs)

      Actually perform the business of activating a user
      account. Receives the ``HttpRequest`` object and any positional
      or keyword arguments passed to the view. Should return the
      activated user account if activation is successful, or any value
      which evaluates ``False`` in boolean context if activation is
      unsuccessful.

   .. method:: get_success_url(request, user)

      Return a URL to redirect to after successful registration, on a
      per-request or per-user basis. If not overridden, will use
      :attr:`~success_url`. Should be a string, the name of a URL
      pattern, or a 3-tuple of arguments suitable for passing to
      Django's ``redirect`` shortcut.
