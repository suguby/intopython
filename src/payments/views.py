# -*- coding: utf-8 -*-
import binascii
import datetime
from collections import defaultdict
from hashlib import md5

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from src.common.views import BaseTemplateView, HttpRedirectException
from src.payments.forms import PreOrderForm, OrderForm
from src.payments.models import Tariff, Orders


class PaymentsView(BaseTemplateView):
    template_name = 'payments/index.html'

    def get_context_data(self, **kwargs):
        context = dict(
            form=PreOrderForm(),
        )
        return context


def get_signature(params, secret_key):
    """
    Base64(Byte(MD5(Windows1251(Sort(Params) + SecretKey))))
    params - list of tuples [('WMI_CURRENCY_ID', 643), ('WMI_PAYMENT_AMOUNT', 10)]
    """
    # https://www.walletone.com/ru/merchant/documentation/
    icase_key = lambda s: str(s).lower()

    lists_by_keys = defaultdict(list)
    for key, value in params:
        lists_by_keys[key].append(value)

    str_buff = b''
    for key in sorted(lists_by_keys, key=icase_key):
        for value in sorted(lists_by_keys[key], key=icase_key):
            str_buff += str(value).encode('1251')
    str_buff += secret_key.encode('1251')
    md5_string = md5(str_buff).digest()
    return binascii.b2a_base64(md5_string)[:-1]


class OrderView(BaseTemplateView):
    template_name = 'payments/order.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_anonymous():
            redirect_to = reverse('registration') + '?next=' + reverse('payments')
            # TODO сделать перенаправление если оно по ридеректу залогинится
            raise HttpRedirectException(redirect_to=redirect_to)
        tariff_id = self.request.GET.get('tariff', None)
        tariff = get_object_or_404(Tariff, id=tariff_id)
        order = Orders.objects.create(
            user=self.request.user,
            tariff=tariff,
            issue_date=datetime.date.today()
        )
        link_pref = '{}://{}'.format(self.request.scheme, get_current_site(self.request))
        data = dict(
            WMI_MERCHANT_ID=settings.WALLETONE_MERCHANT_ID,
            WMI_PAYMENT_AMOUNT='{:.2f}'.format(tariff.cost),
            WMI_CURRENCY_ID='643',
            WMI_PAYMENT_NO=order.id,
            WMI_DESCRIPTION='Оплата счета №{}'.format(order.id),
            WMI_SUCCESS_URL=link_pref + reverse('payment_success'),
            WMI_FAIL_URL=link_pref + reverse('payment_fail'),
            WMI_RECIPIENT_LOGIN=self.request.user.email,
            order_id=order.id,
            user_id=self.request.user.id,
        )
        data['WMI_SIGNATURE'] = get_signature(params=data.items(), secret_key=settings.WALLETONE_TOKEN)
        form = OrderForm(data=data)
        context = dict(form=form, tariff=tariff)
        return context
