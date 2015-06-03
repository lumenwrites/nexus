# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='story',
            field=models.ForeignKey(to='stories.Story', related_name='chapters', default=''),
        ),
    ]
