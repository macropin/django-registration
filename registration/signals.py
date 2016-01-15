from django.conf import settings
from django.contrib.auth import login, get_backends
from django.dispatch import Signal


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])


def login_user(sender, user, request, **kwargs):
    """ Automatically authenticate the user when activated  """
    backend = get_backends()[0]  # Hack to bypass `authenticate()`.
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    request.session['REGISTRATION_AUTO_LOGIN'] = True
    request.session.modified = True

if getattr(settings, 'REGISTRATION_AUTO_LOGIN', False):
    user_activated.connect(login_user)
