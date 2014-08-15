# coding: utf-8
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from registration.views import LoginView

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^accounts/profile/', TemplateView.as_view(template_name='registration/registration_complete.html'), name='profile'),
)
