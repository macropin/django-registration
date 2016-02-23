.. _upgrade:

Upgrade guide
=============

The |version| release of |project| is not compatible with the legacy
django-registration (previously maintained by James Bennett).


Django version requirement
--------------------------

As of |version|, |project| requires Django 1.7 or newer;
older Django releases may work, but are officially unsupported. Additionally,
|project| officially supports Python 2.7, 3.3, 3.4, and 3.5.


Backwards-incompatible changes
------------------------------

Version 1.4
```````````

- Remove unnecessary `_RequestPassingFormView`.
  See `#56 <https://github.com/macropin/django-registration/pull/56>`_. Please
  ensure that you update any subclassed views to reference ``self.request``
  instead of accepting ``request`` as an argument.

Version 1.3
```````````
- Django 1.7 or newer is required. Please ensure you upgrade your Django
  version before upgrading.

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
