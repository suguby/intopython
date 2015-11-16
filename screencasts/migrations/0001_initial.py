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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Заголовок', max_length=128, default='')),
                ('video', models.TextField(verbose_name='Видео', default='')),
                ('summary', models.TextField(verbose_name='Конспект', null=True)),
                ('status', models.CharField(verbose_name='Статус', choices=[('draft', 'Черновик'), ('publ', 'Опубликовано'), ('hided', 'Скрыто')], max_length=16, default='draft')),
                ('created_at', models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)),
            ],
            options={
                'db_table': 'screencasts',
            },
        ),
        migrations.CreateModel(
            name='ScreencastSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Заголовок', max_length=128, default='')),
                ('created_at', models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)),
            ],
            options={
                'db_table': 'screencast_sections',
            },
        ),
        migrations.AddField(
            model_name='screencast',
            name='section',
            field=models.ForeignKey(verbose_name='Раздел', to='screencasts.ScreencastSection'),
        ),
    ]
