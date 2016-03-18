# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from src.registration.views import RegistrationView, RegistrationSuccessView, ProfileView

urlpatterns = [
    url(r'^$', RegistrationView.as_view(), name='registration'),
    url(r'^success/$', RegistrationSuccessView.as_view(), name='registration_success'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url('^', include('django.contrib.auth.urls')),
]
