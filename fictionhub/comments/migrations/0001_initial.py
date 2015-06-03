# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('body', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('comment_type', models.CharField(default='Comment', max_length=64, choices=[('1', 'Comment'), ('2', 'Review')])),
                ('parent', models.ForeignKey(blank=True, to='comments.Comment', default=None, related_name='children', null=True)),
            ],
        ),
    ]
