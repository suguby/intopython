# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Screencast',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(verbose_name='Заголовок', default='', max_length=128)),
                ('video', models.TextField(verbose_name='Видео', default='')),
                ('summary', models.TextField(verbose_name='Конспект', null=True)),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('publ', 'Опубликовано'), ('hided', 'Скрыто')], verbose_name='Статус', default='draft', max_length=16)),
                ('created_at', models.DateTimeField(verbose_name='Создано', auto_now_add=True)),
                ('modified_at', models.DateTimeField(verbose_name='Изменено', auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScreencastSection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(verbose_name='Заголовок', default='', max_length=128)),
            ],
            options={
                'db_table': 'sc_sections',
            },
        ),
        migrations.AddField(
            model_name='screencast',
            name='section',
            field=models.ForeignKey(verbose_name='Раздел', to='screencasts.ScreencastSection'),
        ),
    ]
