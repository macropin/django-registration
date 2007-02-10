import datetime, random, sha
from django.db import models
from django.core.mail import send_mail
from django.template import Context, loader
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings


class RegistrationManager(models.Manager):
    """
    Custom manager for the RegistrationProfile model,
    making it easier to manage profiles.
    
    """
    def create_inactive_user(self, username, password, email, send_email=True):
        """
        Creates a new User and a new RegistrationProfile
        for that User, generates an activation key, and mails
        it.

        Pass ``send_email=False`` to disable sending the email.
        
        """
        # Create the user.
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()
        
        # Generate a salted SHA1 hash to use as a key.
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+new_user.username).hexdigest()

        # Create the profile.
        new_profile = self.create(user=new_user,
                                  activation_key=activation_key)

        if send_email:
            # Send the activation email.
            current_domain = Site.objects.get_current().domain
            subject = "Activate your new account at %s" % current_domain
            message_template = loader.get_template('registration/activation_email.txt')
            message_context = Context({ 'site_url': 'http://%s/' % current_domain,
                                        'activation_key': activation_key,
                                        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS })
            message = message_template.render(message_context)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
        return new_user

    def activate_user(self, activation_key):
        """
        Given the activation key, makes a User's account active if
        the activation key is valid and has not expired.
        
        Returns the User if successful, or False if the account was
        not found or the key had expired.
        
        """
        try:
            user_profile = self.get(activation_key=activation_key)
        except Profile.DoesNotExist:
            return False
        if not user_profile.activation_key_expired():
            # Account exists and has a non-expired key. Activate it.
            user = user_profile.user
            user.is_active = True
            user.save()
            return user
        return False


class RegistrationProfile(models.Model):
    """
    Simple profile model for a User, storing a registration
    date and an activation key for the account.

    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that
    you do so. This model is intended solely to store some data
    needed for user registration, and can do that regardless of
    what you set in ``AUTH_PROFILE_MODULE``, so if you want to
    use user profiles in a project, it's far better to develop
    a customized model for that purpose and just let this one
    handle registration.
    
    """
    user = models.ForeignKey(User, unique=True)
    activation_key = models.CharField(maxlength=40)
    key_generated = models.DateTimeField()
    
    objects = RegistrationManager()

    class Admin:
        pass
    
    def save(self):
        if not self.id:
            self.key_generated = datetime.datetime.now()
        super(RegistrationProfile, self).save()
    
    def __str__(self):
        return "User profile for %s" % self.user.username
    
    def activation_key_expired(self):
        """
        Determines whether this Profile's activation key has expired, based
        on the value of the setting ``ACCOUNT_ACTIVATION_DAYS``.
        
        """
        return self.key_generated + datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS) <= datetime.datetime.now()
