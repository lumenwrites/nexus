# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0003_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='hub',
            name='slug',
            field=models.SlugField(max_length=64, default=''),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=256, default='', unique=True),
        ),
        migrations.AlterField(
            model_name='hub',
            name='title',
            field=models.CharField(max_length=64),
        ),
    ]
