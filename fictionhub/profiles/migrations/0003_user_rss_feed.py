# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150613_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rss_feed',
            field=models.CharField(max_length=128, null=True, default='', blank=True),
        ),
    ]
