# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0015_user_external_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True, default='', max_length=256)),
                ('published', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True, default='', max_length=256)),
                ('published', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('score', models.IntegerField(default=0)),
                ('author', models.ForeignKey(related_name='stories', to=settings.AUTH_USER_MODEL)),
                ('hubs', models.ManyToManyField(blank=True, related_name='stories', to='chaoslegion.Hub')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='story',
            field=models.ForeignKey(related_name='chapters', to='chaoslegion.Story'),
        ),
    ]
