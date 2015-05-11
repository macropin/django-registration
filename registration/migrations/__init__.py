"""
Django migrations for django-registration-redux

This package does not contain South migrations. 

These are Django native migrations. They require Django > 1.7.

"""

SOUTH_ERROR_MESSAGE = """\n
For South support, customize the SOUTH_MIGRATION_MODULES setting like so:

    SOUTH_MIGRATION_MODULES = {
        'registration': 'registration.south_migrations',
    }
"""

# Ensure the user is not using Django 1.6 or below with South
try:
    from django.db import migrations  # noqa
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
