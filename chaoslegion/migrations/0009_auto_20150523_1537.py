# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0008_auto_20150522_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='downvoted',
            field=models.ManyToManyField(related_name='downvoters', blank=True, to='chaoslegion.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='hubs',
            field=models.ManyToManyField(related_name='posts', blank=True, to='chaoslegion.Hub'),
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscribed_to',
            field=models.ManyToManyField(related_name='subscribers', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='upvoted',
            field=models.ManyToManyField(related_name='upvoters', blank=True, to='chaoslegion.Post'),
        ),
    ]
