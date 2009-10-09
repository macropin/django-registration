.. _views:
.. module:: registration.views

Registration views
==================

In order to allow users to register using whatever workflow is
implemented by the :ref:`registration backend <backend-api>` in use,
django-registration provides two views. Both are designed to allow
easy configurability without writing or rewriting view code.

.. function:: activate(request, backend[, template_name[, success_url[, extra_context[, **kwargs]]]])

   Activate a user's account, for workflows which require a separate
   activation step.

   The actual activation of the account will be delegated to the
   backend specified by the ``backend`` keyword argument; the
   backend's ``activate()`` method will be called, passing the
   ``HttpRequest`` and any keyword arguments captured from the URL,
   and will be assumed to return a ``User`` if activation was
   successful, or a value which evaluates to ``False`` in boolean
   context if not.

   Upon successful activation, the backend's
   ``post_activation_redirect()`` method will be called, passing the
   ``HttpRequest`` and the activated ``User`` to determine the URL to
   redirect the user to. To override this, pass the argument
   ``success_url`` (see below).

   On unsuccessful activation, will render the template
   ``registration/activate.html`` to display an error message; to
   override thise, pass the argument ``template_name`` (see below).

   **Context**

   The context will be populated from the keyword arguments captured
   in the URL. This view uses ``RequestContext``, so variables
   populated by context processors will also be present in the
   context.

   :param backend: The dotted Python path to the backend class to use.
   :type backend: string
   :param extra_context: Optionally, variables to add to the template
      context. Any callable object in this dictionary will be called
      to produce the final result which appears in the context.
   :type extra_context: dict
   :param template_name: Optional. A custom template name to use. If
      not specified, this will default to
      ``registration/activate.html``.
   :type template_name: string
   :param **kwargs: Any keyword arguments captured from the URL, such
      as an activation key, which will be passed to the backend's
      ``activate()`` method.


.. function:: register(request, backend[, success_url[, form_class[, disallowed_url[, template_name[, extra_context]]]]])

   Allow a new user to register an account.

   The actual registration of the account will be delegated to the
   backend specified by the ``backend`` keyword argument. The backend
   is used as follows:

   1. The backend's ``registration_allowed()`` method will be called,
      passing the ``HttpRequest``, to determine whether registration
      of an account is to be allowed; if not, a redirect is issued to
      a page indicating that registration is not permitted.

   2. The form to use for account registration will be obtained by
      calling the backend's ``get_form_class()`` method, passing the
      ``HttpRequest``. To override this, pass the keyword argument
      ``form_class``.

   3. If valid, the form's ``cleaned_data`` will be passed (as keyword
      arguments, and along with the ``HttpRequest``) to the backend's
      ``register()`` method, which should return a ``User`` object
      representing the new account.

   4. Upon successful registration, the backend's
      ``post_registration_redirect()`` method will be called, passing
      the ``HttpRequest`` and the new ``User``, to determine the URL
      to redirect to. To override this, pass the keyword argument
      ``success_url``.

   **Context**

   ``form``
        The form instance being used to collect registration data.

   This view uses ``RequestContext``, so variables populated by
   context processors will also be present in the context.

   :param backend: The dotted Python path to the backend class to use.
   :type backend: string
   :param disallowed_url: The URL to redirect to if registration is
      not permitted (e.g., if registration is closed). This should be
      a string suitable for passing as the ``to`` argument to
      `Django's "redirect" shortcut
      <http://docs.djangoproject.com/en/dev/topics/http/shortcuts/#redirect>`_. If
      not specified, this will default to ``registration_disallowed``.
   :type disallowed_url: string
   :param extra_context: Optionally, variables to add to the template
      context. Any callable object in this dictionary will be called
      to produce the final result which appears in the context.
   :type extra_context: dict
   :param form_class: The form class to use for registration; this
      should be some subclass of ``django.forms.Form``. If not
      specified, the backend's ``get_form_class()`` method will be
      called to obtain the form class.
   :type form_class: subclass of ``django.forms.Form``
   :param success_url: The URL to redirect to after successful
      registration. This should be a string suitable for passing as
      the ``to`` argument to `Django's "redirect" shortcut
      <http://docs.djangoproject.com/en/dev/topics/http/shortcuts/#redirect>`_. If
      not specified, the backend's ``post_registration_redirect()``
      method will be called to obtain the URL.
   :type success_url: string
   :param template_name: Optional. A custom template name to use. If
      not specified, this will default to
      ``registration/registration_form.html``.
   :type template_name: string
