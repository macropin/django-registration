from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='index'),

    url(r'^accounts/',
        include('registration.backends.simple.urls')),

    url(r'^accounts/profile/',
        TemplateView.as_view(template_name='profile.html'),
        name='profile'),

    url(r'^login/',
        'django.contrib.auth.views.login',
        name='login')
)