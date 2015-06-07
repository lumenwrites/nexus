# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20150603_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='imported',
            field=models.BooleanField(default=False),
        ),
    ]
