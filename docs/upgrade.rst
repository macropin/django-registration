.. _upgrade:

Upgrade guide
=============

The |version| release of |project| is not compatible with the legacy
django-registration (previously maintained by James Bennett).


Django version requirement
--------------------------

As of |version|, |project| requires Django 1.4 or newer;
older Django releases may work, but are officially unsupported.


Backwards-incompatible changes
------------------------------

Version 1.2
```````````
- **Native migration support breaks South compatibility**: An initial native
  migration for Django > 1.7 has been provided. South users will need to
  configure a null migration with (`SOUTH_MIGRATION_MODULES`) in
  `settings.py` as shown below:

  ::

      SOUTH_MIGRATION_MODULES = {
          'registration': 'registration.south_migrations',

- **register method in RegistrationView has different parameters**: The
  parameters of the`register` method in RegistrationView have changed.

Version 1.1
```````````

- **base.html template required**: A `base.html` template is now assumed to
  exist. Please ensure that your project provides one for |project| to inherit
  from.
- **HTML email templates**: |project| now uses HTML email templates. If you
  previously customized text email templates, you need to do the same with
  the new HTML templates.
