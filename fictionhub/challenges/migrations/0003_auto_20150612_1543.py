# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_challenge_challenge_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='challenge_state',
            new_name='state',
        ),
    ]
