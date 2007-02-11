"""
URLConf for Django user registration.

Recommended usage is to use a call to ``include()`` in your
project's root URLConf to include this URLConf for any URL
begninning with '/accounts/'.

"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout
from views import activate, register

urlpatterns = patterns('',
                       (r'^activate/(?P<activation_key>[a-fA-F0-9]+)/$', activate),
                       (r'^login/$', login, {'template_name': 'registration/login.html'}),
                       (r'^logout/$', logout, {'template_name': 'registration/logout.html'}),
                       (r'^register/$', register),
                       (r'^register/complete/$', direct_to_template, {'template': 'registration/registration_complete.html'}),
                       )
