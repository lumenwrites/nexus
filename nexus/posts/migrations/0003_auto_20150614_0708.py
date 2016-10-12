# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20150613_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('number',)},
        ),
        migrations.RemoveField(
            model_name='post',
            name='posttype',
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(default='story', blank=True, choices=[('story', 'Story'), ('chapter', 'Chapter')], max_length=64),
        ),
    ]
