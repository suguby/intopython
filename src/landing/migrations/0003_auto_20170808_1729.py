# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_lendingregistration_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lendingregistration',
            name='details',
            field=models.TextField(blank=True, max_length=1024, null=True, verbose_name='Расскажите о себе или задайте вопросы (необязательно)'),
        ),
        migrations.AlterField(
            model_name='lendingregistration',
            name='email',
            field=models.EmailField(max_length=64, verbose_name='Ваш email'),
        ),
        migrations.AlterField(
            model_name='lendingregistration',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Ваше имя'),
        ),
        migrations.AlterField(
            model_name='lendingregistration',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Ваш номер телефона или skype-логин (необязательно)'),
        ),
        migrations.AlterField(
            model_name='lendingregistration',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('accepted', 'Оплативший'), ('rejected', 'Отказник')], default='new', max_length=16, verbose_name='Статус'),
        ),
    ]
