# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hubs', '0001_initial'),
        ('stories', '0002_chapter_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='author',
            field=models.ForeignKey(default='', to=settings.AUTH_USER_MODEL, related_name='stories'),
        ),
        migrations.AddField(
            model_name='story',
            name='hubs',
            field=models.ManyToManyField(blank=True, to='hubs.Hub', related_name='stories'),
        ),
    ]
