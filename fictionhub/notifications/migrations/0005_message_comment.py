# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20150614_0708'),
        ('notifications', '0004_message_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='comment',
            field=models.ForeignKey(to='comments.Comment', default=None, null=True, blank=True),
        ),
    ]
