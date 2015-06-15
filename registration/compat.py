import sys
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
from django.utils import six

try:
    from django.contrib.sites.requests import RequestSite
except ImportError:
    # Django < 1.7
    from django.contrib.sites.models import RequestSite

try:
    from django.apps import apps
    is_app_installed, get_model = apps.is_installed, apps.get_model
except ImportError:
    # Django < 1.7
    from django.db.models import loading
    from django.core.exceptions import ImproperlyConfigured

    def is_app_installed(app_name):
        try:
            loading.get_app(app_name.rsplit('.', 1)[-1])
            return True
        except ImproperlyConfigured:
            return False
    get_model = loading.get_model

get_site_model = lambda: get_model('sites', 'Site')

try:
    from django.utils.module_loading import import_string
except ImportError:
    def import_string(dotted_path):
        """
        COPIED FROM DJANGO 1.7 (django.utils.module_loading.import_string)
        Import a dotted module path and return the attribute/class designated
        by the last name in the path. Raise ImportError if the import failed.
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            msg = "%s doesn't look like a module path" % dotted_path
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError:
            msg = 'Module "%s" does not define a "%s" attribute/class' % (
                dotted_path, class_name)
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

__all__ = ['import_string', 'RequestSite', 'is_app_installed',
           'get_model', 'get_site_model']
