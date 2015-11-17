# -*- coding: utf-8 -*-

from django.conf.urls import url

from blogs.views import BlogsView

urlpatterns = [
    url(r'^$', BlogsView.as_view(), name='blogs'),
]
