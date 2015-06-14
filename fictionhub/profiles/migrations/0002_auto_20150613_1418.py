# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_post'),
        ('posts', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comments_downvoted',
            field=models.ManyToManyField(blank=True, to='comments.Comment', related_name='downvoters'),
        ),
        migrations.AddField(
            model_name='user',
            name='comments_upvoted',
            field=models.ManyToManyField(blank=True, to='comments.Comment', related_name='upvoters'),
        ),
        migrations.AddField(
            model_name='user',
            name='downvoted',
            field=models.ManyToManyField(blank=True, to='posts.Post', related_name='downvoters'),
        ),
        migrations.AddField(
            model_name='user',
            name='upvoted',
            field=models.ManyToManyField(blank=True, to='posts.Post', related_name='upvoters'),
        ),
    ]
