# -*- coding: utf-8 -*-
from django.forms import forms
from markdownx.fields import MarkdownxFormField


class ScreencastForm(forms.Form):

    myfield = MarkdownxFormField()
