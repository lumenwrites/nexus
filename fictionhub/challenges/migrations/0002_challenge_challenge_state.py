# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='challenge_state',
            field=models.IntegerField(default=1, choices=[(1, 'Open'), (2, 'Voting'), (2, 'Completed')]),
        ),
    ]
