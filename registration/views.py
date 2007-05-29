"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration.forms import RegistrationForm
from registration.models import RegistrationProfile


def activate(request, activation_key):
    """
    Activates a ``User``'s account, if their key is valid and hasn't
    expired.

    Context::
        account
            The ``User`` object corresponding to the account,
            if the activation was successful.

        expiration_days
            The number of days for which activation keys stay valid.

    Template::
        registration/activate.html
    
    """
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    return render_to_response('registration/activate.html',
                              { 'account': account,
                                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=RequestContext(request))


def register(request, success_url='/accounts/register/complete/', profile_callback=None):
    """
    Allows a new user to register an account.
    
    On successful registration, an email will be sent to the new user
    with an activation link to click to make the account active. This
    view will then redirect to ``success_url``, which defaults to
    '/accounts/register/complete/'. This application has a URL pattern
    for that URL and routes it to the ``direct_to_template`` generic
    view to display a short message telling the user to check their
    email for the account activation link.
    
    To enable creation of a site-specific user profile object for the
    new user, pass a function which will create the profile object as
    the keyword argument ``profile_callback``. See
    ``RegistrationManager.create_inactive_user`` for details on what
    this function should do.
    
    Context::
        form
            The registration form
    
    Template::
        registration/registration_form.html
    
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = RegistrationProfile.objects.create_inactive_user(username=form.cleaned_data['username'],
                                                                        password=form.cleaned_data['password1'],
                                                                        email=form.cleaned_data['email'],
                                                                        profile_callback=profile_callback)
            return HttpResponseRedirect(success_url)
    else:
        form = RegistrationForm()
    return render_to_response('registration/registration_form.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

