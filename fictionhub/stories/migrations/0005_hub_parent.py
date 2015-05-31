# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_auto_20150531_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='hub',
            name='parent',
            field=models.ForeignKey(related_name='children', default=None, to='stories.Hub', null=True, blank=True),
        ),
    ]
