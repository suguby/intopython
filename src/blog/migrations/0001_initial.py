# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-04 17:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('articles.article',),
        ),
    ]