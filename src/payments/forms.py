# -*- coding: utf-8 -*-
import datetime

from django.forms import Form, ChoiceField, IntegerField, CharField, HiddenInput

from src.payments.models import Tariff


class HiddenField(CharField):
    widget = HiddenInput


def tariff_choices():
    today = datetime.date.today()
    tarifs = Tariff.objects.filter(valid_till__gte=today).order_by('paid_days')
    choices = [(t.id, '{} руб, {} дней'.format(t.cost, t.paid_days)) for t in tarifs]
    return choices


class PreOrderForm(Form):
    tariff = ChoiceField(label='Выберите подходящий тариф', choices=tariff_choices)


class OrderForm(Form):
    WMI_MERCHANT_ID = HiddenField()
    WMI_PAYMENT_AMOUNT = HiddenField()
    WMI_CURRENCY_ID = HiddenField()
    WMI_PAYMENT_NO = HiddenField()
    WMI_DESCRIPTION = HiddenField()
    WMI_SUCCESS_URL = HiddenField()
    WMI_FAIL_URL = HiddenField()
    WMI_EXPIRED_DATE = HiddenField()
    WMI_RECIPIENT_LOGIN = HiddenField()
    WMI_SIGNATURE = HiddenField()
    order_id = HiddenField()
    user_id = HiddenField()
