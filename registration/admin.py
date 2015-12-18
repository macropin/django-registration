from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.requests import RequestSite
from django.apps import apps

from .models import RegistrationProfile
from .users import UsernameField


class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__{0}'.format(UsernameField()),
                     'user__first_name', 'user__last_name')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not already
        activated.

        """
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.

        """
        if apps.is_installed('django.contrib.sites'):
            site = apps.get_model('sites', 'Site').objects.get_current()
        else:
            site = RequestSite(request)

        for profile in queryset:
            user = profile.user
            RegistrationProfile.objects.resend_activation_mail(user.email, site)

    resend_activation_email.short_description = _("Re-send activation emails")


admin.site.register(RegistrationProfile, RegistrationAdmin)
