# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_migrate_activatedstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisedRegistrationProfile',
            fields=[
                ('registrationprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='registration.RegistrationProfile')),
            ],
            bases=('registration.registrationprofile',),
        ),
    ]
