.. _upgrade:

Upgrade guide
=============

The |version| release of |project| is compatible with the legacy
django-registration (previously maintained by James Bennett)


Django version requirement
--------------------------

As of |version|, |project| requires Django 1.4 or newer;
older Django releases may work, but are officially unsupported.


Backwards-incompatible changes
------------------------------

**Base Templates**
A `base.html` template is now assumed to exist. Please ensure that your project provides on for |project| to inherit
from.

**South Users**
Initial migration for Django > 1.7 has been provided. South users will need to configure a null migration with
(`SOUTH_MIGRATION_MODULES`) in `settings.py` as shown below:


    SOUTH_MIGRATION_MODULES = {
        'registration': 'registration.south_migrations',
    }