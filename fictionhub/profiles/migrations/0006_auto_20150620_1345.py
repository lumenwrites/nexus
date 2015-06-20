# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20150617_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='website',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
