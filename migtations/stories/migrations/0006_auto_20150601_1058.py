# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0005_hub_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
