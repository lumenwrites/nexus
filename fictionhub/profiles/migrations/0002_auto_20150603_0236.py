# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20150603_0234'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='downvoted',
            field=models.ManyToManyField(related_name='downvoters', blank=True, to='stories.Story'),
        ),
        migrations.AddField(
            model_name='user',
            name='upvoted',
            field=models.ManyToManyField(related_name='upvoters', blank=True, to='stories.Story'),
        ),
    ]
