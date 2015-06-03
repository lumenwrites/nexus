# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20150603_0055'),
        ('stories', '0009_hub_users_can_create_children'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='story',
        ),
        migrations.RemoveField(
            model_name='hub',
            name='parent',
        ),
        migrations.AlterField(
            model_name='story',
            name='hubs',
            field=models.ManyToManyField(blank=True, related_name='stories', to='hubs.Hub'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Hub',
        ),
    ]
