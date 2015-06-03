# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20150603_0234'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default='', related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='chapter',
            field=models.ForeignKey(null=True, default=None, related_name='comments', blank=True, to='stories.Chapter'),
        ),
        migrations.AddField(
            model_name='comment',
            name='story',
            field=models.ForeignKey(null=True, default=None, related_name='comments', blank=True, to='stories.Story'),
        ),
    ]
