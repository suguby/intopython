# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screencasts', '0003_auto_20151117_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='screencast',
            name='body',
            field=models.TextField(null=True, verbose_name='Содержание статьи'),
        ),
        migrations.AlterField(
            model_name='screencast',
            name='section',
            field=models.ForeignKey(verbose_name='Раздел', to='screencasts.ScreencastSection', related_name='screencasts'),
        ),
    ]
