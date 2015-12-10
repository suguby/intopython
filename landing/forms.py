# -*- coding: utf-8 -*-

from django import forms


class BootStrapField(forms.CharField):

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({'class': "form-control",
                 'placeholder': self.label,
                 'aria-describedby': "basic-addon1"})
        return attrs


class RegisterForm(forms.Form):
    name = BootStrapField(label='Ваше имя')
    email = BootStrapField(label='Введите email')
    phone = BootStrapField(label='Введите номер телефона (необязательно)')
