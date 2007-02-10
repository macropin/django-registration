This is a fairly simple user-registration application for Django,
designed to make allowing user signups as painless as possible. It
requires a recent Subversion checkout of Django, since it uses
newforms and a couple other post-0.95 additions. Aside from that, it
has no external dependencies.

Here's how it works:

First, use a call to ``include()`` in your project's root URLConf file
to include this application's URLs under '/accounts/'. For example,
this line in your root URLConf should do the trick:

    (r'^accounts/', include('registration.urls')),

User registration is handled by means of a model called
``RegistrationProfile``; you can, if you like, use it as the value of
your ``AUTH_PROFILE_MODULE`` setting, but you don't have to for it to
work and I personally recommend developing a separate user profile
module customized to your site if you want the functionality of
``AUTH_PROFILE_MODULE``.

Each ``RegistrationProfile`` is tied to an instance of ``auth.User``,
and carries two piece of metadata: an activation key for their account
and the date on which the key was generated.

You'll need to add a new setting to your project's settings file,
called ``ACCOUNT_ACTIVATION_DAYS``; this should be the number of days
after which an unused activation key will expire. Each
``RegistrationProfile`` has a method called ``activation_key_expired``
which will check this setting, its own key-generation date, and return
whether the key is still valid.

There's a custom manager on ``RegistrationProfile`` which has a couple
convenience methods:

  * ``create_inactive_user`` does exactly what it sounds like. Given a
    username, a password and an email address, it will save a new
    ``User`` instance and set ``is_active=False`` on that
    ``User``. Then it will generate a new ``RegistrationProfile`` with
    an activation key, and email an activation link to the user to
    activate their account.

 * ``activate_user`` also does exactly what it sounds like; given an
   activation key, it looks up the ``User`` and activates their
   account so they can log in.

Included with this app (in the "templates" directory) is a sample set
of templates; here's what they do:

  * ``registration_form.html`` is for user signup, and shows the
    registration form.

  * ``registration_complete.html`` is a simple page to display telling
    the user they've signed up and will be getting an activation
    email.

 * ``activation_email.txt`` is the template the app will use to
   generate the text of the activation email; it has access to three
   variables:
   
     ``current_domain`` -- the domain name of the site the new user
     registered for.
     
     ``activation_key`` -- their activation key.
     
     ``expiration_days`` -- the number of days for which the key will
     be valid.

  * ``activate.html`` is the template for the account activation view.

  * ``login.html`` is a simple login template.

  * ``logout.html`` is a simple template to display after a user logs
    out.

So long as you have ``django.template.loaders.app_directories.load_template_source``
in your ``TEMPlATE_LOADERS`` setting, Django should pick up these
templates automatically without any need to move them.