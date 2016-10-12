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
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(default='', max_length=256)),
                ('body', models.TextField(default='', null=True, blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('message_type', models.CharField(choices=[('message', 'Message'), ('comment', 'Comment'), ('review', 'Review'), ('reply', 'Reply'), ('subscriber', 'Subscriber'), ('upvote', 'Upvote')], default='message', blank=True, max_length=64)),
                ('isread', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(default='', to=settings.AUTH_USER_MODEL, related_name='out_messages')),
                ('to_user', models.ForeignKey(default='', to=settings.AUTH_USER_MODEL, related_name='in_messages')),
            ],
        ),
    ]
