# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20150614_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('story', 'Story'), ('chapter', 'Chapter'), ('thread', 'Thread'), ('prompt', 'Prompt'), ('challenge', 'Challenge')], max_length=64, blank=True, default='story'),
        ),
        migrations.AlterField(
            model_name='post',
            name='state',
            field=models.CharField(choices=[('open', 'Open'), ('voting', 'Voting'), ('completed', 'Completed')], max_length=64, blank=True, null=True, default=None),
        ),
    ]
