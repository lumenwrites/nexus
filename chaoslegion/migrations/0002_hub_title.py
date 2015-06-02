# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hub',
            name='title',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
