# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField, CharField, HiddenInput

from src.registration.models import MyUser


class MyUserCreationForm(UserCreationForm):
    email = EmailField(max_length=254, required=True)

    class Meta:
        model = MyUser
        fields = ("email", )


class MyUserAuthenticationForm(AuthenticationForm):
    username = EmailField(max_length=254, required=True)
