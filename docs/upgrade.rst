.. _upgrade:

Upgrade guide
=============

The |version| release of |project| is not compatible with the legacy
django-registration (previously maintained by James Bennett). Major backwards
incompatible changes will be recorded here, but for a full list of changes
between versions you should refer to the `CHANGELOG
<https://github.com/macropin/django-registration/blob/master/CHANGELOG>`_.

Django version requirement
--------------------------

As of |version|, |project| requires Django 1.11 or newer;
older Django releases may work, but are officially unsupported. Additionally,
|project| officially supports Python 2.7, 3.4, and 3.5, 3.6.


Backwards-incompatible changes
------------------------------

Version 2.4
```````````

- None

Version 2.3
```````````

- None


Version 2.2
```````````

- None


Version 2.1
```````````

- None


Version 2.0
```````````

- Removed support for Django < 1.11.
- Removed `registration/urls.py` in favor of
  `registration/backends/default/urls.py`


Version 1.9
```````````
- Change of return signature of
  ``RegistrationProfileManager.activate_user``. A tuple containing the
  User instance and a boolean of whether or not said user was activated
  is now returned.


Version 1.8
```````````

- None

Version 1.7
```````````

- None

Version 1.6
```````````

- None

Version 1.5
```````````

- Support for Django 1.7 is removed, and Django 1.8 or newer is required.
- Change signature of ``RegistrationProfileManager.activate_user``.
  ``site`` is now a required positional argument.
  See `#244 <https://github.com/macropin/django-registration/pull/244>`_.

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
