# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_post_approved'),
        ('notifications', '0003_remove_message_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='story',
            field=models.ForeignKey(blank=True, null=True, to='posts.Post', default=None),
        ),
    ]
