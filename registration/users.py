from django.conf import settings

from .compat import get_model

try:
    from django.contrib.auth import get_user_model
    UserModel = get_user_model
except ImportError:
    UserModel = lambda: get_model('auth', 'User')


def UserModelString():
    try:
        return settings.AUTH_USER_MODEL
    except AttributeError:
        return 'auth.User'


def UsernameField():
    return getattr(UserModel(), 'USERNAME_FIELD', 'username')
