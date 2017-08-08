# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import BlogView, BlogDetailView, BlogEditView

urlpatterns = [
    url(r'^$', BlogView.as_view(), name='blog'),
    url(r'^add/$', BlogEditView.as_view(), name='blog_add'),
    url(r'^(?P<slug>.*)/edit/$', BlogEditView.as_view(), name='blog_edit'),
    url(r'^(?P<slug>.*)$', BlogDetailView.as_view(), name='blog_detail'),

]
