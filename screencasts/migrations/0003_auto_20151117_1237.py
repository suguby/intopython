# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screencasts', '0002_auto_20151117_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screencast',
            name='slug',
            field=models.SlugField(verbose_name='Слаг', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='screencastsection',
            name='slug',
            field=models.SlugField(verbose_name='Слаг', blank=True, null=True),
        ),
    ]
