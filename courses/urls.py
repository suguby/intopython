# -*- coding: utf-8 -*-

from django.conf.urls import url

from courses.views import CoursesView, CoursesProgramView, CoursesAuthorView

urlpatterns = [
    url(r'^$', CoursesView.as_view(), name='courses'),
    url(r'^author$', CoursesAuthorView.as_view(), name='courses_author'),
    url(r'^program/$', CoursesProgramView.as_view(), name='courses_program'),
]
