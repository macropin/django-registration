"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration import get_backend


def activate(request,
             template_name='registration/activate.html',
             extra_context=None, backend=get_backend(),
             **kwargs):
    """
    Activate a user's account.

    The actual activation of the account will be delegated to the
    backend specified by the ``REGISTRATION_BACKEND`` setting
    (although this can be overridden; see argument list below); the
    backend's ``activate()`` method will be called, passing any
    keyword arguments captured from the URL, and will be assumed to
    return a ``User`` if activation was successful, or a value which
    evaluates to ``False`` in boolean context if not.

    **Optional arguments**

    ``backend``
        An instance of a registration backend. If specified, will be
        used in place of the backend specified by the
        ``REGISTRATION_BACKEND`` setting.

    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.
    
    ``template_name``
        A custom template to use. If not specified, this will default
        to ``registration/activate.html``.
    
    **Context:**
    
    ``account``
        The ``User`` object corresponding to the account, if the
        activation was successful. ``False`` if the activation was not
        successful.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/activate.html or ``template_name`` keyword argument.
    
    """
    account = backend.activate(request, **kwargs)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account, },
                              context_instance=context)


def register(request, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None, backend=get_backend()):
    """
    Allow a new user to register an account.

    The actual registration of the account will be delegated to the
    backend specified by the ``REGISTRATION_BACKEND`` setting
    (although this can be overridden; see argument list below); it
    will be used as follows:

    1. The backend's ``registration_allowed()`` method will be called,
       passing the ``HttpRequest``, to determine whether registration
       of an account is to be allowed; if not, a redirect is issued to
       the view corresponding to the named URL pattern
       ``registration_disallowed``. To override this, see the list of
       optional arguments for this view (below).

    2. The form to use for account registration will be obtained by
       calling the backend's ``get_form_class()`` method, passing the
       ``HttpRequest``. To override this, see the list of optional
       arguments for this view (below).

    3. If valid, the form's ``cleaned_data`` will be passed (as
       keyword arguments, and along with the ``HttpRequest``) to the
       backend's ``register()`` method, which should return the new
       ``User`` object.

    4. Upon successful registration, the backend's
       ``post_registration_redirect()`` method will be called, passing
       the ``HttpRequest`` and the new ``User``, to determine the URL
       to redirect the user to. To override this, see the list of
       optional arguments for this view (below).
    
    **Required arguments**
    
    None.
    
    **Optional arguments**

    ``backend``
        An instance of a registration backend. If specified, will be
        used in place of the backend specified by the
        ``REGISTRATION_BACKEND`` setting.

    ``disallowed_url``
        URL to redirect to if registration is not permitted for the
        current ``HttpRequest``. Must be a value which can legally be
        passed to ``django.shortcuts.redirect``. If not supplied, this
        will be whatever URL corresponds to the named URL pattern
        ``registration_disallowed``.
    
    ``form_class``
        The form class to use for registration. If not supplied, this
        will be retrieved from the registration backend.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    ``success_url``
        URL to redirect to after successful registration. Must be a
        value which can legally be passed to
        ``django.shortcuts.redirect``. If not supplied, this will be
        retrieved from the registration backend.
    
    ``template_name``
        A custom template to use. If not supplied, this will default
        to ``registration/registration_form.html``.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = backend.register(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)
