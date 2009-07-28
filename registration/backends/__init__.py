from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# TODO: When Python 2.7 is released this becomes a try/except falling
# back to Django's implementation.
from django.utils.importlib import import_module

def get_backend(path=None):
    """
    Return an instance of a registration backend.

    If specified, the backend will be imported from ``path``, which
    should be the full dotted Python import path to the backend
    class. If ``path`` is not specified, the backend will be imported
    based on the value of the setting ``REGISTRATION_BACKEND``, which
    should similarly be a full dotted Python import path.

    If the backend cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    
    """
    if path is None:
        if not hasattr(settings, 'REGISTRATION_BACKEND') or not settings.REGISTRATION_BACKEND:
            raise ImproperlyConfigured('Error loading registration backend: no backend specified (have you provided a value for the REGISTRATION_BACKEND setting?)')
        path = settings.REGISTRATION_BACKEND
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration backend %s: "%s"' % (module, e))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration backend named "%s"' % (module, attr))
    return backend_class()
