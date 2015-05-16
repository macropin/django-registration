from django.conf import settings


def UserModel():
    try:
        from django.contrib.auth import get_user_model
        return get_user_model()
    except ImportError:
        from django.contrib.auth.models import User
        return User


def UserModelString():
    try:
        return settings.AUTH_USER_MODEL
    except AttributeError:
        return 'auth.User'


def UsernameField():
    return getattr(UserModel(), 'USERNAME_FIELD', 'username')
