# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='chapter',
            field=models.ForeignKey(related_name='comments', to='stories.Chapter', blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(related_name='children', to='stories.Comment', blank=True, default=None, null=True),
        ),
    ]
