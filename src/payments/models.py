# -*- coding: utf-8 -*-

from django.db import models
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


class Orders(AbstractModel):
    STATUSES = Choices(
        ('new', 'Выставлен'),
        ('paid', 'Оплачен'),
        ('closed', 'Закрыт'),
    )

    user = models.ForeignKey(MyUser)
    tariff = models.ForeignKey(Tariff)
    status = models.CharField(max_length=32, choices=STATUSES, default=STATUSES.new)
    issue_date = models.DateField()
    payment_date = models.DateField()
    amount = models.FloatField()

    class Meta:
        db_table = 'orders'

    _str_template = '{user} / {tariff} / {status} / {summ}'
