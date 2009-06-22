"""
URLs used in the unit tests for django-registration.

You should not attempt to use these URLs in any sort of real or
development environment; instead, use
``registration/backends/default/urls.py``. This URLConf includes those
URLs, and also adds several additional URLs which serve no purpose
other than to test that optional keyword arguments are properly
handled.

"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import activate
from registration.views import register


urlpatterns = patterns('',
                       # Test the 'activate' view with custom template
                       # name.
                       url(r'^activate-with-template-name/(?P<activation_key>\w+)/$',
                           activate,
                           {'template_name': 'registration/test_template_name.html'},
                           name='registration_test_activate_template_name'),
                       # Test the 'activate' view with
                       # extra_context_argument.
                       url(r'^activate-extra-context/(?P<activation_key>\w+)/$',
                           activate,
                           {'extra_context': {'foo': 'bar', 'callable': lambda: 'called'}},
                           name='registration_test_activate_extra_context'),
                       (r'', include('registration.backends.default.urls')),
                       # Test the 'register' view with custom template
                       # name.
                       url(r'^register-with-template-name/$',
                           register,
                           {'template_name': 'registration/test_template_name.html'},
                           name='registration_test_register_template_name'),
                       # Test the'register' view with extra_context
                       # argument.
                       url(r'^register-extra-context/$',
                           register,
                           {'extra_context': {'foo': 'bar', 'callable': lambda: 'called'}},
                           name='registration_test_register_extra_context'),
                       # Test the 'register' view with custom URL for
                       # closed registration.
                       url(r'^register-with-disallowed-url/$',
                           register,
                           {'disallowed_url': 'registration_test_custom_disallowed'},
                           name='registration_test_register_disallowed_url'),
                       # Set up a pattern which will correspond to the
                       # custom 'disallowed_url' above.
                       url(r'^custom-disallowed/$',
                           direct_to_template,
                           {'template': 'registration/registration_closed.html'},
                           name='registration_test_custom_disallowed'),
                       )
