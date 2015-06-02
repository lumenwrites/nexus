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
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(default='', unique=True, max_length=256)),
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
            name='Hub',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('slug', models.SlugField(default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(default='', unique=True, max_length=256)),
                ('published', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='stories')),
                ('hubs', models.ManyToManyField(to='stories.Hub', related_name='stories', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='story',
            field=models.ForeignKey(to='stories.Story', related_name='chapters'),
        ),
    ]
