# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hubs', '0003_hub_order'),
        ('profiles', '0009_user_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribed_to_hubs',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to='hubs.Hub'),
        ),
    ]
