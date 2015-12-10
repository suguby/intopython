# -*- coding: utf-8 -*-

from django.db import models
from model_utils import Choices


class LendingRegistration(models.Model):
    STATUSES = Choices(('new', 'Новый'), ('accepted', 'Оплативший'),  ('rejected', 'Отказник'), )

    name = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=32, null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUSES, default=STATUSES.new)
    register_at = models.DateTimeField(auto_now_add=True)
