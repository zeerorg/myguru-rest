# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='teacher_id',
            field=models.IntegerField(),
        ),
    ]
