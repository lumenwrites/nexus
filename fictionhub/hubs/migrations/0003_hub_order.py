# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hubs', '0002_hub_hub_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hub',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
