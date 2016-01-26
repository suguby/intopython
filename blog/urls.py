# -*- coding: utf-8 -*-

from django.conf.urls import url

from blog.views import BlogView, BlogDetailView

urlpatterns = [
    url(r'^$', BlogView.as_view(), name='blog'),
    url(r'^(?P<slug>.*)$', BlogDetailView.as_view(), name='blog_detail'),
]
