from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from models import RegistrationProfile
from forms import RegistrationForm

def activate(request, activation_key):
    """
    Activates a user's account, if their key is valid
    and hasn't expired.

    Context::
        account
            The ``User`` object corresponding to the account,
            if the activation was successful.

        expiration_days
            The number of days for which activation keys stay valid.

    Template::
        registration/activate.html
    
    """
    activation_key = activation_key.lower()
    account = RegistrationProfile.objects.activate_user(activation_key)
    return render_to_response('registration/activate.html',
                              {'account': account,
                               'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=RequestContext(request))

def register(request, success_url='/accounts/register/complete/'):
    """
    Allows a new user to register an account.

    On successful registration, an email will be sent to the new
    user with an activation link to click to make the account
    active. This view will then redirect to ``success_url``,
    which defaults to '/accounts/register/complete/'. This
    application has a URL pattern for that URL and routes it to
    the ``direct_to_template`` generic view to display a short
    message telling the user to check their email for the
    account activation link.
    
    Context::
        form
            The registration form
    
    Template::
        registration/registration_form.html
    
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = RegistrationProfile.objects.create_inactive_user(username=form.clean_data['username'],
                                                            password=form.clean_data['password1'],
                                                            email=form.clean_data['email'])
            return HttpResponseRedirect(success_url)
    else:
        form = RegistrationForm()
    return render_to_response('registration/registration_form.html',
                              { 'form': form },
                              context_instance=RequestContext(request))
