# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput, Textarea
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget

from src.common.forms import FormCheckSlugMixin
from src.screencasts.models import Screencast


class ScreencastForm(ModelForm, FormCheckSlugMixin):
    body = MarkdownxFormField()

    class Meta:
        model = Screencast
        fields = (
            'title',
            'summary',
            'video',
            'image',
            'body',
            'status',
            'by_subscription',
            'section',
        )
        widgets = dict(
            title=TextInput(attrs={'size': 60}),
            summary=Textarea(attrs=dict(rows='5', cols='50')),
            video=Textarea(attrs=dict(rows='3', cols='50')),
            body=MarkdownxWidget(attrs=dict(rows='10', cols='50')),
        )
