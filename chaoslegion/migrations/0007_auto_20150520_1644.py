# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0006_auto_20150520_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='hubs',
        ),
        migrations.AddField(
            model_name='post',
            name='hubs',
            field=models.ManyToManyField(blank=True, related_name='posts', to='chaoslegion.Hub', null=True),
        ),
    ]
