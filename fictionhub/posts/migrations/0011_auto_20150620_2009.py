# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20150620_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=256, default=''),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('slug', 'number')]),
        ),
    ]
