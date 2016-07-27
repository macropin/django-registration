from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='index'),

    url(r'^accounts/',
        include('registration.backends.admin_approval.urls')),

    url(r'^accounts/profile/',
        TemplateView.as_view(template_name='profile.html'),
        name='profile'),

    url(r'^login/',
        auth_views.login,
        name='login'),

    url(r'^admin/',
        include(admin.site.urls),
        name='admin'),
]
