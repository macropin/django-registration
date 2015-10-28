import sys

from importlib import import_module
from django.utils import six
from django.contrib.sites.requests import RequestSite
from django.apps import apps

is_app_installed, get_model = apps.is_installed, apps.get_model
get_site_model = lambda: get_model('sites', 'Site')

from django.utils.module_loading import import_string

__all__ = ['import_string', 'RequestSite', 'is_app_installed',
           'get_model', 'get_site_model']
