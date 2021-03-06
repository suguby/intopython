# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import CoursesView, CoursesProgramView, CoursesAuthorView, CoursesSignView, CoursesSignedView

urlpatterns = [
    url(r'^$', CoursesView.as_view(), name='courses'),
    url(r'^author$', CoursesAuthorView.as_view(), name='courses_author'),
    url(r'^program/$', CoursesProgramView.as_view(), name='courses_program'),
    url(r'^sign/$', CoursesSignView.as_view(), name='courses_sign'),
    url(r'^signed/$', CoursesSignedView.as_view(), name='courses_signed'),
]
