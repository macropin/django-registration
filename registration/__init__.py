from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# TODO: When Python 2.7 is released this becomes a try/except falling
# back to Django's implementation.
from django.utils.importlib import import_module

def get_backend():
    """
    Return an instance of the registration backend for use on this
    site, as determined by the ``REGISTRATION_BACKEND`` setting. Raise
    ``django.core.exceptions.ImproperlyConfigured`` if the specified
    backend cannot be located, or if no backend is specified.
    
    """
    if not hasattr(settings, 'REGISTRATION_BACKEND') or not settings.REGISTRATION_BACKEND:
        raise ImproperlyConfigured('Error loading registration backend: no backend specified (have you provided a value for the REGISTRATION_BACKEND setting?)')
    i = settings.REGISTRATION_BACKEND.rfind('.')
    module, attr = settings.REGISTRATION_BACKEND[:i], settings.REGISTRATION_BACKEND[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration backend %s: "%s"' % (module, e))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration backend named "%s"' % (module, attr))
    return backend_class()
