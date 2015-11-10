# -*- coding: utf-8 -*-

from django.conf.urls import url

from screencasts.views import ScreencastsListView

urlpatterns = [
    url(r'', ScreencastsListView.as_view(), name='screencasts'),
]
