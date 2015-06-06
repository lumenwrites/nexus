# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20150606_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_type',
            field=models.IntegerField(default=1, choices=[(1, 'Comment'), (2, 'Review')]),
        ),
    ]
