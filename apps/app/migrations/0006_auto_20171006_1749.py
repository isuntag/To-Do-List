# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-06 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_task_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=0),
        ),
    ]