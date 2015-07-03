# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_user_rational'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shadowban',
            field=models.BooleanField(default=False),
        ),
    ]
