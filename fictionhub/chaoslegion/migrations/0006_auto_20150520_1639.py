# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0005_user_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='subscribed_to',
            field=models.ManyToManyField(related_name='subscribers', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
