# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_post_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='daily',
            field=models.BooleanField(default=False),
        ),
    ]