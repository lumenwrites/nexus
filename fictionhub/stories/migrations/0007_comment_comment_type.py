# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0006_auto_20150601_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_type',
            field=models.CharField(choices=[('1', 'Comment'), ('2', 'Review')], default='Comment', max_length=64),
        ),
    ]
