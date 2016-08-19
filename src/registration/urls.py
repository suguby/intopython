# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from src.registration.forms import MyUserAuthenticationForm
from src.registration.views import RegistrationView, ProfileView, LogoutView, ProfileProAccessView

urlpatterns = [
    url(r'^$', RegistrationView.as_view(), name='registration'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/pro_access$', ProfileProAccessView.as_view(), name='pro_access'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.login,
        dict(authentication_form=MyUserAuthenticationForm),
        name='login'),
    url('^', include('django.contrib.auth.urls')),
]
