# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0012_auto_20150524_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.TextField(max_length=32, blank=True),
        ),
    ]
