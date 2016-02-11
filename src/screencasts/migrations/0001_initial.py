# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screencast',
            fields=[
                ('article_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, auto_created=True, to='articles.Article')),
                ('video', models.TextField(default='', verbose_name='Видео')),
            ],
            options={
                'db_table': 'screencasts',
            },
            bases=('articles.article',),
        ),
        migrations.CreateModel(
            name='ScreencastSection',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', verbose_name='Заголовок', max_length=128)),
                ('slug', models.SlugField(blank=True, verbose_name='Слаг', null=True)),
                ('position', models.IntegerField(default=0, verbose_name='Позиция')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Создано', auto_now_add=True)),
                ('modified_at', models.DateTimeField(null=True, verbose_name='Изменено', auto_now=True)),
            ],
            options={
                'db_table': 'screencast_sections',
            },
        ),
        migrations.AddField(
            model_name='screencast',
            name='section',
            field=models.ForeignKey(related_name='screencasts', verbose_name='Раздел', to='src.screencasts.ScreencastSection'),
        ),
    ]
