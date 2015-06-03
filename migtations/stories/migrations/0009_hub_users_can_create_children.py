# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0008_hub_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='hub',
            name='users_can_create_children',
            field=models.BooleanField(default=True),
        ),
    ]
