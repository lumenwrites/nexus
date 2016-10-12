# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_user_category_to_import'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='category_to_import',
            new_name='categories_to_import',
        ),
    ]
