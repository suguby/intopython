# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from src.registration.views import RegistrationView, ProfileView, LogoutView

urlpatterns = [
    url(r'^$', RegistrationView.as_view(), name='registration'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url('^', include('django.contrib.auth.urls')),
]
