# -*- coding: utf-8 -*-
from django.forms import ModelForm
from markdownx.fields import MarkdownxFormField

from src.screencasts.models import Screencast


class ScreencastForm(ModelForm):

    class Meta:
        model = Screencast
        fields = ('title', 'summary', 'by_subscription', 'image', 'status', 'video')

    body = MarkdownxFormField()
