# -*- coding: utf-8 -*-

from django.conf.urls import url

from courses.views import CoursesView

urlpatterns = [
    url(r'^$', CoursesView.as_view(), name='courses'),
]
