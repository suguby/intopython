#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from forums.views import CategoryListView, ForumDetailView, TopicDetailView, TopicCreateView, PostCreateView

urlpatterns = [
     url(r'^forum/$', CategoryListView.as_view(), name='category_list'),
     url(r'^forum/(?P<pk>[0-9]+)/$', ForumDetailView.as_view(), name='forum_detail'),
     url(r'^topic/(?P<pk>[0-9]+)/$', TopicDetailView.as_view(), name='topic_detail'),
     url(r'^forum/(?P<forum_id>\d+)/create/$', login_required(TopicCreateView.as_view()), name='topic_create'),
     url(r'^topic/(?P<pk>\d+)/create/$', login_required(PostCreateView.as_view()), name='post_create'),
]