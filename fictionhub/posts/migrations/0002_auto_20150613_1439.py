# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hubs', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts', default=''),
        ),
        migrations.AddField(
            model_name='post',
            name='hubs',
            field=models.ManyToManyField(related_name='posts', blank=True, to='hubs.Hub'),
        ),
    ]
