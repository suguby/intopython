# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-12 08:00
from __future__ import unicode_literals

from django.db import IntegrityError
from django.db import migrations
from django.db import models
from django.db import transaction


class OldUser(models.Model):
    email = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField()

    class Meta:
        db_table = 'auth_user'


def move_users(apps, schema_editor):
    MyUser = apps.get_model("registration", "MyUser")
    for old_user in OldUser.objects.all():
        try:
            with transaction.atomic():
                MyUser.objects.create(
                    email=old_user.email,
                    password=old_user.password,
                    date_joined=old_user.date_joined,
                    name=old_user.username,
                    is_active=old_user.is_active,
                    is_admin=old_user.is_staff,
                    is_superuser=old_user.is_superuser
                )
        except IntegrityError:
            print('Duplicate user email {}. Skipped.'.format(old_user.email))


def delete_users(apps, schema_editor):
    MyUser = apps.get_model("registration", "MyUser")
    with transaction.atomic():
        MyUser.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(move_users, delete_users),
    ]
