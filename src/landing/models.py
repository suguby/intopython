# -*- coding: utf-8 -*-

from django.db import models
from model_utils import Choices

from src.common.models import AbstractModel


class LendingRegistration(AbstractModel):
    STATUSES = Choices(('new', 'Новый'), ('accepted', 'Оплативший'),  ('rejected', 'Отказник'), )

    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=32, null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUSES, default=STATUSES.new)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='lending_registrations'

    _str_template = '{name} / {email} / {registered_at}'
