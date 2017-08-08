# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import Form

from src.articles.models import Article
from src.common.utils import get_slug


class FormCheckSlugMixin(Form):

    def clean_title(self):
        title = self.cleaned_data['title']
        _filter = Q(slug=get_slug(title))
        if self.instance and self.instance.id:
            _filter &= ~Q(id=self.instance.id)
        for article in Article.objects.filter(_filter):
            raise ValidationError('Slug for new title exists! article id {}'.format(article.id))
        return title


