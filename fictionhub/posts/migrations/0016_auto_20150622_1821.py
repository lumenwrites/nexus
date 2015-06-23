# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20150622_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(max_length=64, default='story', choices=[('story', 'Story'), ('chapter', 'Chapter'), ('thread', 'Thread'), ('prompt', 'Prompt'), ('challenge', 'Challenge'), ('wiki', 'Wiki')], blank=True),
        ),
    ]
