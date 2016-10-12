# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20150614_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reddit_url',
            field=models.URLField(max_length=256, default='', blank=True, null=True),
        ),
    ]
