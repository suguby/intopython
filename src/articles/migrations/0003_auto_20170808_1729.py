# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20160811_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.CharField(blank=True, db_index=True, max_length=128, unique=True, verbose_name='Слаг'),
        ),
    ]
