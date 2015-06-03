# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=64)),
                ('slug', models.SlugField(default='', max_length=64)),
                ('users_can_create_children', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, max_length=512)),
                ('parent', models.ForeignKey(blank=True, to='hubs.Hub', default=None, related_name='children', null=True)),
            ],
        ),
    ]
