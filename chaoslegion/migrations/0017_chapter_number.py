# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaoslegion', '0016_auto_20150528_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
