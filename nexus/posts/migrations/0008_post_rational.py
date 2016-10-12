# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_post_reddit_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rational',
            field=models.BooleanField(default=False),
        ),
    ]
