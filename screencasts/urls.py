# -*- coding: utf-8 -*-

from django.conf.urls import url

from screencasts.views import ScreencastsListView, ScreencastDetailView, ScreencastsSearchView

urlpatterns = [
    url(r'^$', ScreencastsListView.as_view(), name='screencasts'),
    url(r'^search/', ScreencastsSearchView.as_view(), name='screencasts_search'),
    url(r'^(?P<slug>.*)$', ScreencastDetailView.as_view(), name='screencast_detail'),
]
