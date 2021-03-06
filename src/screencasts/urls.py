# -*- coding: utf-8 -*-

from django.conf.urls import url

from src.screencasts.views import (
    ScreencastsListView, ScreencastDetailView, ScreencastsSearchView, ProVersionView, ScreencastEditView,
    ScreencastCreateView)

urlpatterns = [
    url(r'^$', ScreencastsListView.as_view(), name='screencasts'),
    url(r'^search/', ScreencastsSearchView.as_view(), name='screencasts_search'),
    url(r'^pro/', ProVersionView.as_view(), name='go_pro'),
    url(r'^add/$', ScreencastCreateView.as_view(), name='screencast_add'),

    url(r'^(?P<slug>.*)/edit/$', ScreencastEditView.as_view(), name='screencast_edit'),
    url(r'^(?P<slug>.*)$', ScreencastDetailView.as_view(), name='screencast_detail'),
]
