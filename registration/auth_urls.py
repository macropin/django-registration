"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""

from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

# Attempt to use the auth class based views if available.
try:
    login_view = auth_views.LoginView.as_view()
    logout_view = auth_views.LogoutView.as_view()
    password_change_view = auth_views.PasswordChangeView.as_view()
    password_change_done_view = auth_views.PasswordChangeDoneView.as_view()
    password_reset_view = auth_views.PasswordResetView.as_view()
    password_reset_complete_view = auth_views.PasswordResetCompleteView.as_view()
    password_reset_done_view = auth_views.PasswordResetDoneView.as_view()
    password_reset_confirm_view = auth_views.PasswordResetConfirmView.as_view()
except AttributeError:
    login_view = auth_views.login
    logout_view = auth_views.logout
    password_change_view = auth_views.password_change
    password_change_done_view = auth_views.password_change_done
    password_reset_view = auth_views.password_reset
    password_reset_complete_view = auth_views.password_reset_complete
    password_reset_done_view = auth_views.password_reset_done
    password_reset_confirm_view = auth_views.password_reset_confirm

urlpatterns = [
    url(r'^login/$',
        login_view,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        logout_view,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^password/change/$',
        password_change_view,
        {'post_change_redirect': reverse_lazy('auth_password_change_done')},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        password_change_done_view,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        password_reset_view,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_done')},
        name='auth_password_reset'),
    url(r'^password/reset/complete/$',
        password_reset_complete_view,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        password_reset_done_view,
        name='auth_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm_view,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_complete')},
        name='auth_password_reset_confirm'),
]
