# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_user_subscribed_to_hubs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_comments',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email_subscriptions',
            field=models.BooleanField(default=True),
        ),
    ]
