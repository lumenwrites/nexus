# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('body', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('comment_type', models.IntegerField(default=1, choices=[(1, 'Comment'), (2, 'Review')])),
                ('rating', models.IntegerField(default=None, choices=[(1, 'Horrible'), (2, 'Bad'), (3, 'Okay'), (4, 'Good'), (5, 'Brilliant')], blank=True, null=True)),
                ('author', models.ForeignKey(default='', related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(default=None, null=True, blank=True, to='comments.Comment', related_name='children')),
            ],
        ),
    ]
