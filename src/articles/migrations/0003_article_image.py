# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-09 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20160418_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Содержание статьи'),
        ),
    ]
