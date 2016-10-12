# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20150620_2028'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('parent', 'slug')]),
        ),
    ]
