# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_message_email_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_type',
            field=models.CharField(max_length=64, default='message', blank=True, choices=[('message', 'Message'), ('comment', 'Comment'), ('review', 'Review'), ('reply', 'Reply'), ('subscriber', 'Subscriber'), ('upvote', 'Upvote'), ('newstory', 'New Story')]),
        ),
    ]
