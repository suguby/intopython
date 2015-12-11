# -*- coding: utf-8 -*-

from django import forms
from django.forms import EmailField


class BootstrapField(forms.CharField):

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'class': "form-control",
            'placeholder': self.label,
            'aria-describedby': "basic-addon1"})
        return attrs


class BootstrapEmailField(EmailField, BootstrapField):
    pass


class RegisterForm(forms.Form):
    name = BootstrapField(label='Ваше имя')
    email = BootstrapEmailField(label='Ваш email')
    phone = BootstrapField(label='Ваш номер телефона или skype-логин (необязательно)', required=False)
