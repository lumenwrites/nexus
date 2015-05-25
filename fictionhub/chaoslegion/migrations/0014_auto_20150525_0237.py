# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0013_user_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='website',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
