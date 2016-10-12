# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='title',
        ),
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(blank=True, related_name='messages', to='notifications.Subject', default=None, null=True),
        ),
    ]
