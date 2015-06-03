# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0010_auto_20150603_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('body', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('comment_type', models.CharField(max_length=64, default='Comment', choices=[('1', 'Comment'), ('2', 'Review')])),
                ('author', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('chapter', models.ForeignKey(blank=True, related_name='comments', to='stories.Chapter', default=None, null=True)),
                ('parent', models.ForeignKey(blank=True, related_name='children', to='comments.Comment', default=None, null=True)),
                ('story', models.ForeignKey(blank=True, related_name='comments', to='stories.Story', default=None, null=True)),
            ],
        ),
    ]
