# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import PaymentsView, OrderView

urlpatterns = [
    url(r'^$', PaymentsView.as_view(), name='payments'),
    url(r'^order/$', OrderView.as_view(), name='order'),
    url(r'^success/$', PaymentsView.as_view(), name='payment_success'),
    url(r'^fail/$', PaymentsView.as_view(), name='payment_fail'),
]
