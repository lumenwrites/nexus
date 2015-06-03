# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(default='', max_length=256, unique=True)),
                ('number', models.IntegerField(default=1)),
                ('published', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(default='', max_length=256, unique=True)),
                ('published', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('score', models.IntegerField(default=0)),
            ],
        ),
    ]
