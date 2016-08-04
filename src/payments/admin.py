# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Tariff, Order

admin.site.register(Tariff)
admin.site.register(Order)
