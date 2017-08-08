# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput, Textarea
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget

from src.blog.models import Blog


class BlogForm(ModelForm):
    body = MarkdownxFormField()

    class Meta:
        model = Blog
        fields = (
            'title',
            'summary',
            'image',
            'body',
            'status',
        )
        widgets = dict(
            title=TextInput(attrs={'size': 60}),
            summary=Textarea(attrs=dict(rows='5', cols='50')),
            video=Textarea(attrs=dict(rows='3', cols='50')),
            body=MarkdownxWidget(attrs=dict(rows='10', cols='50')),
        )

