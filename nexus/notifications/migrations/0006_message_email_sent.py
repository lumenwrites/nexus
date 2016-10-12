# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_message_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
