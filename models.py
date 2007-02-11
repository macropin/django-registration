"""
A registration profile model and associated manager.

The RegistrationProfile model and especially its custom manager
implement nearly all the logic needed to handle user registration
and account activation, so before implementing something in a view
or form, check here to see if they can handle it.

Also, be sure to see the note on RegistrationProfile about use of
the ``AUTH_PROFILE_MODULE`` setting.

"""

import datetime, random, re, sha
from django.db import models
from django.template import Context, loader
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings


class RegistrationManager(models.Manager):
    """
    Custom manager for the RegistrationProfile model.
    
    The two methods defined here should be all that's needed to
    handle account creation and activation.
    
    """
    def activate_user(self, activation_key):
        """
        Given the activation key, makes a User's account active if
        the activation key is valid and has not expired.
        
        Returns the User if successful, or False if the account was
        not found or the key had expired.
        
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point even trying to look it up
        # in the DB.
        if re.match('[a-f0-9]{40}', activation_key):
            try:
                user_profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not user_profile.activation_key_expired():
                # Account exists and has a non-expired key. Activate it.
                user = user_profile.user
                user.is_active = True
                user.save()
                return user
        return False
    
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
        
        # And finally create the profile.
        new_profile = self.create(user=new_user,
                                  activation_key=activation_key)
        
        if send_email:
            from django.core.mail import send_mail
            current_domain = Site.objects.get_current().domain
            subject = "Activate your new account at %s" % current_domain
            message_template = loader.get_template('registration/activation_email.txt')
            message_context = Context({ 'site_url': 'http://%s/' % current_domain,
                                        'activation_key': activation_key,
                                        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS })
            message = message_template.render(message_context)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
        return new_user
    
    def delete_expired_users(self):
        """
        Removes unused profiles and their associated accounts.

        This is provided largely as a convenience for maintenance purposes;
        if a RegistrationProfile's key expires without the account being
        activated, then both the RegistrationProfile and the associated User
        become clutter in the database, and (more importantly) it won't be
        possible for anyone to ever come back and claim the username. For best
        results, set this up to run regularly as a cron job.
        
        If you have a User whose account you want to keep in the database even
        though it's inactive (say, to prevent a troublemaker from accessing or
        re-creating his account), just delete that User's RegistrationProfile
        and this method will leave it alone.
        
        """
        for profile in self.all():
            user = profile.user
            if profile.activation_key_expired and not user.is_active:
                user.delete() # Removing the User will remove the RegistrationProfile, too.


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
