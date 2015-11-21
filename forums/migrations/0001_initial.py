# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('position', models.IntegerField(verbose_name='Position', default=0)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('position', models.IntegerField(verbose_name='Position', default=0)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('is_closed', models.BooleanField(verbose_name='Is closed', default=False)),
                ('category', models.ForeignKey(related_name='forums', to='forums.Category')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('updated', models.DateTimeField(verbose_name='Updated', auto_now=True)),
                ('body', models.TextField(verbose_name='Body')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('forum', models.ForeignKey(related_name='topics', to='forums.Forum')),
                ('last_post', models.ForeignKey(blank=True, null=True, verbose_name='Last post', to='forums.Post', related_name='forum_last_post')),
            ],
            options={
                'ordering': ['-last_post__created'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(related_name='posts', to='forums.Topic'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name='forum_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
