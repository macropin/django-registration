from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^$', 'test_app.views.index', name='index'),

    (r'^accounts/', include('registration.backends.default.urls')),

    url(r'^login/', 'django.contrib.auth.views.login', name='login'),

    url(r'^accounts/profile/', TemplateView.as_view(template_name='registration/registration_complete.html'), name='profile'),
)