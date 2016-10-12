# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20150614_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='state',
            field=models.CharField(blank=True, max_length=64, choices=[('story', 'Story'), ('chapter', 'Chapter')], default=None, null=True),
        ),
    ]
