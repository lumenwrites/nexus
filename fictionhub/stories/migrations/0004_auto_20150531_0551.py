# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20150531_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='story',
            field=models.ForeignKey(blank=True, related_name='comments', to='stories.Story', null=True, default=None),
        ),
    ]
