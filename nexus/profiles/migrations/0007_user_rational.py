# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20150620_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rational',
            field=models.BooleanField(default=True),
        ),
    ]
