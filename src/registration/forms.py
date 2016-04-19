# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField, CharField, HiddenInput, PasswordInput
from django.utils.translation import ugettext_lazy as _

from src.registration.models import MyUser


class MyUserCreationForm(UserCreationForm):
    email = EmailField(max_length=254, required=True)
    next = CharField(max_length=254, required=True, widget=HiddenInput)  # TODO выпилить

    class Meta:
        model = MyUser
        fields = ("email", )


class MyUserAuthenticationForm(AuthenticationForm):
    email = EmailField(max_length=254, required=True)
    password = CharField(label=_("Password"), widget=PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(email) and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }
