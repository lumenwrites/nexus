# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150614_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='state',
            field=models.CharField(default=None, max_length=64, blank=True, choices=[('story', 'Story'), ('chapter', 'Chapter')]),
        ),
    ]
