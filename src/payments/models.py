# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import PROTECT
from model_utils import Choices

from src.common.models import AbstractModel
from src.registration.models import MyUser


class Tariff(AbstractModel):
    cost = models.FloatField(verbose_name='Стоимость')
    paid_days = models.IntegerField(verbose_name='Кол-во дней доступа')
    valid_till = models.DateField(verbose_name='Срок действия тарифа')

    class Meta:
        db_table = 'tariffs'

    _str_template = '{cost} / {paid_days} / {valid_till}'


class Order(AbstractModel):
    STATUSES = Choices(
        ('new', 'Выставлен'),
        ('paid', 'Оплачен'),
        ('fail', 'Отменен'),
        ('closed', 'Закрыт'),
    )

    user = models.ForeignKey(MyUser)
    tariff = models.ForeignKey(Tariff, on_delete=PROTECT)
    status = models.CharField(max_length=32, choices=STATUSES, default=STATUSES.new)
    issue_date = models.DateField()  # TODO лучше переделать на DatetimeField
    payment_date = models.DateField(null=True)
    amount = models.FloatField(null=True)
    external_payment_id = models.CharField(max_length=128, null=True)
    external_user_wallet_id = models.CharField(max_length=32, null=True)
    commission_amount = models.FloatField(null=True)

    class Meta:
        db_table = 'orders'

    _str_template = '{user_id} / {tariff_id} / {status} / {amount}'
