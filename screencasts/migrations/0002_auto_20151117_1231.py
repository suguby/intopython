# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screencasts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='screencast',
            name='position',
            field=models.IntegerField(verbose_name='Позиция', default=0),
        ),
        migrations.AddField(
            model_name='screencast',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Слаг'),
        ),
        migrations.AddField(
            model_name='screencastsection',
            name='position',
            field=models.IntegerField(verbose_name='Позиция', default=0),
        ),
        migrations.AddField(
            model_name='screencastsection',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Слаг'),
        ),
    ]
