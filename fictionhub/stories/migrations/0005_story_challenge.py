# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
        ('stories', '0004_story_imported'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='challenge',
            field=models.ForeignKey(to='challenges.Challenge', default=None, related_name='stories', null=True, blank=True),
        ),
    ]
