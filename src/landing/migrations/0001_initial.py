# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LendingRegistration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=64)),
                ('phone', models.CharField(blank=True, max_length=32, null=True)),
                ('status', models.CharField(max_length=16, default='new', choices=[('new', 'Новый'), ('accepted', 'Оплативший'), ('rejected', 'Отказник')])),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'lending_registrations',
            },
        ),
    ]
