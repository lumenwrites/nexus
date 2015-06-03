# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150601_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='comments_downvoted',
            field=models.ManyToManyField(blank=True, related_name='downvoters', to='comments.Comment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='comments_upvoted',
            field=models.ManyToManyField(blank=True, related_name='upvoters', to='comments.Comment'),
        ),
    ]
