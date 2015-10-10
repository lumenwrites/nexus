# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_user_new_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_messages',
            field=models.BooleanField(verbose_name='Send me email notifications when someone sends me a personal message.', default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_subscribers',
            field=models.BooleanField(verbose_name='Send me email notifications when someone subscribes to my stories.', default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_upvotes',
            field=models.BooleanField(verbose_name='Send me email notifications when someone upvotes my story.', default=True),
        ),
    ]
