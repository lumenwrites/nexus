# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20150622_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('post', 'Post'), ('story', 'Story'), ('chapter', 'Chapter'), ('thread', 'Thread'), ('prompt', 'Prompt'), ('challenge', 'Challenge'), ('wiki', 'Wiki')], blank=True, default='story', max_length=64),
        ),
    ]
