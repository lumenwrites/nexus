# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0014_auto_20150525_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='external_url',
            field=models.BooleanField(default=False),
        ),
    ]
