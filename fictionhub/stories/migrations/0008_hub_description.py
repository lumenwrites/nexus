# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0007_comment_comment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hub',
            name='description',
            field=models.TextField(blank=True, max_length=512),
        ),
    ]
