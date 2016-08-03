# -*- coding: utf-8 -*-
import binascii
import datetime
import logging
from collections import defaultdict
from hashlib import md5

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404

from src.common.views import BaseTemplateView, HttpRedirectException
from src.payments.forms import PreOrderForm, OrderForm, tariff_choices
from src.payments.models import Tariff, Orders

log = logging.getLogger('intopython')


class PaymentsView(BaseTemplateView):
    template_name = 'payments/index.html'

    def get_context_data(self, **kwargs):
        form = PreOrderForm()
        tariffs = tariff_choices()
        context = dict(
            form=form,
            first_tariff=tariffs[0][1],
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
        order, created = Orders.objects.get_or_create(
            user=self.request.user,
            status=Orders.STATUSES.new,
            defaults=dict(
                tariff=tariff,
                issue_date=datetime.date.today()
            ),
        )
        if not created:
            order.tariff = tariff
            order.issue_date = datetime.date.today()
            order.save()
        link_pref = '{}://{}'.format(self.request.scheme, get_current_site(self.request))
        data = dict(
            WMI_MERCHANT_ID=settings.WALLETONE_MERCHANT_ID,
            WMI_PAYMENT_AMOUNT='{:.2f}'.format(tariff.cost),
            WMI_CURRENCY_ID='643',
            WMI_PAYMENT_NO=order.id,
            WMI_DESCRIPTION='Доступ к PRO-версии сайта intopython.ru сроком на {} дней'.format(tariff.paid_days),
            WMI_SUCCESS_URL=link_pref + reverse('payment_success'),
            WMI_FAIL_URL=link_pref + reverse('payment_fail'),
            WMI_RECIPIENT_LOGIN=self.request.user.email,
            WMI_CULTURE_ID='ru-RU',
            order_id=order.id,
            user_id=self.request.user.id,
        )
        data['WMI_SIGNATURE'] = get_signature(params=data.items(), secret_key=settings.WALLETONE_TOKEN)
        form = OrderForm(data=data)
        context = dict(form=form, tariff=tariff)
        log.info("OrderView: new order {}".format(order))
        return context


class PaymentTransactionView(BaseTemplateView):
    template_name = 'payments/transaction.html'

    def post(self, request, *args, **kwargs):
        # https://www.walletone.com/ru/merchant/documentation/#step5
        # WMI_MERCHANT_ID	Идентификатор интернет-магазина.
        # WMI_PAYMENT_AMOUNT	Сумма заказа
        # WMI_COMMISSION_AMOUNT	Сумма удержанной комиссии
        # WMI_CURRENCY_ID	Идентификатор валюты заказа (ISO 4217)
        # WMI_TO_USER_ID	Двенадцатизначный номер кошелька плательщика.
        # WMI_PAYMENT_NO	Идентификатор заказа в системе учета интернет-магазина.
        # WMI_ORDER_ID	Идентификатор заказа в системе учета Единой кассы.
        # WMI_DESCRIPTION	Описание заказа.
        # WMI_SUCCESS_URL WMI_FAIL_URL	Адреса (URL) страниц интернет-магазина, на которые будет отправлен покупатель после успешной или неуспешной оплаты.
        # WMI_EXPIRED_DATE	Срок истечения оплаты в западно-европейском часовом поясе (UTC+0).
        # WMI_CREATE_DATE WMI_UPDATE_DATE	Дата создания и изменения заказа в западно-европейском часовом поясе (UTC+0).
        # WMI_ORDER_STATE	Состояние оплаты заказа: Accepted  — заказ оплачен;
        # WMI_SIGNATURE	Подпись уведомления об оплате, сформированная с использованием «секретного ключа» интернет-магазина.

        data = request.POST
        log.info("PaymentTransactionView: {}".format(data))
        wmi_signature = data.pop('WMI_SIGNATURE')
        signature = get_signature(params=data.items(), secret_key=settings.WALLETONE_TOKEN)
        if wmi_signature != signature:
            log.info("PaymentTransactionView: Invalid signature")
            return self.render_to_response(context=dict(success=False, description='Invalid signature'))
        wmi_payment_no = request.POST.get('WMI_PAYMENT_NO')
        order_id = request.POST.get('order_id', wmi_payment_no)
        qs = Orders.objects.filter(id=order_id).select_related('user', 'tariff')
        if not len(qs):
            description = 'No order with id {} sended as WMI_PAYMENT_NO'.format(order_id)
            log.info("PaymentTransactionView: {}".format(description))
            return self.render_to_response(
                context=dict(success=False, description=description))
        order = qs[0]
        user_id = request.POST.get('user_id')
        if user_id and int(user_id) != order.user.id:
            log.info("PaymentTransactionView: user_id {} != order.user.id {}".format(user_id, order.user.id))
        order.external_payment_id = request.POST.get('WMI_ORDER_ID')
        order.external_user_wallet_id = request.POST.get('WMI_TO_USER_ID')
        order.commission_amount = request.POST.get('WMI_COMMISSION_AMOUNT')
        log.info("PaymentTransactionView: order {}".format(order))
        WMI_ORDER_STATE = request.POST.get('WMI_ORDER_STATE')
        if WMI_ORDER_STATE == 'Accepted':
            order.status = Orders.STATUSES.paid
            with transaction.atomic():
                last_access = order.user.access_till if order.user.access_till else datetime.date.today()
                order.user.access_till = last_access + datetime.timedelta(days=order.tariff.paid_days)
                order.user.save()
                order.save()
                log.info("PaymentTransactionView: updated access to user_id {} until {}".format(
                    order.user.id, order.user.access_till))
        else:
            order.status = Orders.STATUSES.fail
            order.save()
            log.info("PaymentTransactionView: WMI_ORDER_STATE {}".format(WMI_ORDER_STATE))
        return self.render_to_response(context=dict(success=True, description=''))


class PaymentSuccessView(BaseTemplateView):
    template_name = 'payments/success.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_anonymous():
            redirect_to = reverse('registration')
            raise HttpRedirectException(redirect_to=redirect_to)
        context = super(PaymentSuccessView, self).get_context_data(**kwargs)
        access_till = self.request.user.access_till
        if access_till:
            access_till = access_till.strftime('%Y-%m-%d')
        context.update(dict(
            access_till=access_till,
            message='Оплата прошла успешно'
        ))
        return context


class PaymentFailView(PaymentSuccessView):

    def get_context_data(self, **kwargs):
        context = super(PaymentFailView, self).get_context_data(**kwargs)
        context['message'] = 'Оплата не удалась'
        return context
