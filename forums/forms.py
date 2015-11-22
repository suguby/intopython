#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class TopicCreateForm(forms.Form):
    topic = forms.CharField(label="Topic", min_length=3)
    message = forms.CharField(label="Сообщение", min_length=3, widget=forms.Textarea())
