# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 16:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0004_auto_20160803_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'Выставлен'), ('paid', 'Оплачен'), ('fail', 'Отменен'), ('closed', 'Закрыт')], default='new', max_length=32)),
                ('issue_date', models.DateTimeField()),
                ('payment_date', models.DateField(null=True)),
                ('amount', models.FloatField(null=True)),
                ('external_payment_id', models.CharField(max_length=128, null=True)),
                ('external_user_wallet_id', models.CharField(max_length=32, null=True)),
                ('commission_amount', models.FloatField(null=True)),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payments.Tariff')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.RemoveField(
            model_name='orders',
            name='tariff',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='user',
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
