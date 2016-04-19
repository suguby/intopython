# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField, CharField, HiddenInput, PasswordInput
from django.utils.translation import ugettext_lazy as _

from src.registration.models import MyUser


class MyUserCreationForm(UserCreationForm):
    email = EmailField(max_length=254, required=True)
    next = CharField(max_length=254, required=True, widget=HiddenInput)

    class Meta:
        model = MyUser
        fields = ("email", )


class MyUserAuthenticationForm(AuthenticationForm):
    username = EmailField(max_length=254, required=True)
    next = CharField(max_length=254, required=True, widget=HiddenInput)
