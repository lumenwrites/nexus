# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_comment_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_type',
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=None, null=True, blank=True, choices=[(1, 'Horrible'), (2, 'Bad'), (3, 'Okay'), (4, 'Good'), (5, 'Brilliant')]),
        ),
    ]
