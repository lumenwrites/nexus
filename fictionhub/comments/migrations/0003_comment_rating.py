# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20150603_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=None, blank=True, null=True),
        ),
    ]
