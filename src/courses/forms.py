# -*- coding: utf-8 -*-

from django import forms
from django.forms import EmailField, CharField


class SignForm(forms.Form):
    name = CharField(label='Ваше имя')
    email = EmailField(label='Ваш email')
    phone = CharField(label='Ваш номер телефона или skype-логин (необязательно)', required=False)
