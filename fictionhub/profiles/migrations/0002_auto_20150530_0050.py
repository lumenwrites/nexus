# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='downvoted',
            field=models.ManyToManyField(blank=True, related_name='downvoters', to='stories.Story'),
        ),
        migrations.AddField(
            model_name='user',
            name='upvoted',
            field=models.ManyToManyField(blank=True, related_name='upvoters', to='stories.Story'),
        ),
    ]
