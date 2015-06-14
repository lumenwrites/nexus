# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(default='', max_length=256, unique=True)),
                ('published', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('imported', models.BooleanField(default=False)),
                ('posttype', models.CharField(default='post', max_length=64, choices=[('post', 'Post'), ('story', 'Story'), ('chapter', 'Chapter'), ('thread', 'Thread'), ('prompt', 'Prompt'), ('challenge', 'Challenge')])),
                ('state', models.IntegerField(default=1, choices=[(1, 'Open'), (2, 'Voting'), (3, 'Completed')])),
                ('number', models.IntegerField(default=1)),
                ('parent', models.ForeignKey(blank=True, related_name='children', default=None, to='posts.Post', null=True)),
            ],
        ),
    ]
