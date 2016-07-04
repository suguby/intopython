# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import (
    PaymentsView, OrderView, PaymentTransactionView, PaymentSuccessView, PaymentFailView)

urlpatterns = [
    url(r'^$', PaymentsView.as_view(), name='payments'),
    url(r'^order/$', OrderView.as_view(), name='order'),
    url(r'^transaction/$', PaymentTransactionView.as_view(), name='payment_transaction'),
    url(r'^success/$', PaymentSuccessView.as_view(), name='payment_success'),
    url(r'^fail/$', PaymentFailView.as_view(), name='payment_fail'),
]
