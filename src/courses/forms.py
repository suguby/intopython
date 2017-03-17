# -*- coding: utf-8 -*-

from django import forms
from django.forms import Textarea

from src.landing.models import LendingRegistration


class SignForm(forms.ModelForm):
    class Meta:
        model = LendingRegistration
        exclude = ('status', 'registered_at', )
        widgets = {
            'details': Textarea(attrs=dict(rows='3', cols='50')),
        }
