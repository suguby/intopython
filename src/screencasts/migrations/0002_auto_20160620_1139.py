# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screencasts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screencastsection',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Слаг'),
        ),
    ]