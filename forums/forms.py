#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class TopicCreateForm(forms.Form):
    topic = forms.CharField(label="Название", min_length=3, widget=forms.TextInput({'class': 'form-control'}))
    message = forms.CharField(label="Сообщение", min_length=3, widget=forms.Textarea({'class': 'form-control'}))
