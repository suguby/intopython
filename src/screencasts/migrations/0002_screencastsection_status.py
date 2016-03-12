# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-11 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screencasts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='screencastsection',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('publ', 'Опубликовано'), ('hided', 'Скрыто')], default='draft', max_length=16, verbose_name='Статус'),
        ),
    ]