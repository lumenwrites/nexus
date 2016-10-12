# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_type',
            field=models.CharField(default='comment', blank=True, choices=[('comment', 'Comment'), ('review', 'Review')], max_length=64),
        ),
    ]
