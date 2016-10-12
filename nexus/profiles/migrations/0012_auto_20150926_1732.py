# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20150926_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enable_dark_interface',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_comments',
            field=models.BooleanField(default=True, verbose_name='Send me email notifications when someone replies to my story or comment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_subscriptions',
            field=models.BooleanField(default=True, verbose_name='Send me email notifications when someone I follow publishes a new story'),
        ),
    ]
