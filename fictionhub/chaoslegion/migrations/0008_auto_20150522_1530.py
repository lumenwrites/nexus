# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0007_auto_20150520_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='upvoted',
            field=models.ManyToManyField(blank=True, to='chaoslegion.Post', null=True, related_name='upvoters'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='submitted_posts'),
        ),
    ]
