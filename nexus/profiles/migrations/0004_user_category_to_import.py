# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_user_rss_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='category_to_import',
            field=models.CharField(blank=True, default='', max_length=128, null=True),
        ),
    ]
