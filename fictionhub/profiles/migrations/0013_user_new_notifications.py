# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20150926_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='new_notifications',
            field=models.BooleanField(default=False),
        ),
    ]
