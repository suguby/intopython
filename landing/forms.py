# -*- coding: utf-8 -*-

from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label='Ваше имя')
    email = forms.CharField(label='Введите email')
    phone = forms.CharField(label='Введите номер телефона (необязательно)')
