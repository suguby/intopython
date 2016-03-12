# -*- coding: utf-8 -*-
from collections import Counter

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import get_object_or_404
from markdown import markdown

from src.common.views import BaseTemplateView
from .models import Screencast, ScreencastSection


class ScreencastsBaseView(BaseTemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sections = ScreencastSection.objects.filter(
            status=ScreencastSection.STATUSES.publ
        ).order_by('position')
        screencasts = Screencast.objects.filter(
            status=Screencast.STATUSES.publ
        ).order_by('-created_at').prefetch_related('tagged_items__tag')
        # TODO уменьшить количество запросов
        slugs_counter = Counter((slug for sc in screencasts for slug in sc.tags.slugs()))
        count_range = slugs_counter.most_common(1)[0][1] / 4.0
        tags = []
        for tag in Screencast.tags.order_by('name'):
            if tag.slug in slugs_counter:
                tag.range = int(5 - slugs_counter[tag.slug] // count_range)
                tags.append(tag)
        context.update(
            sections=sections,
            screencasts=screencasts,
            tags=tags,
            blt=__builtins__,
        )
        return context


class ScreencastsListView(ScreencastsBaseView):
    template_name = 'screencasts/index.html'
    PAGE_SIZE = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screencasts = context['screencasts']
        section_filter = self.request.GET.get('section')
        tag_filter = self.request.GET.get('tag')
        screencasts_filter = ''
        if section_filter:
            screencasts = screencasts.filter(section__slug=section_filter)
            screencasts_filter += 'section={}&'.format(section_filter)
        elif tag_filter:
            screencasts = screencasts.filter(tags__slug=tag_filter)
            screencasts_filter += 'tag={}&'.format(tag_filter)
        paginator = Paginator(screencasts, self.PAGE_SIZE)
        try:
            screencasts = paginator.page(number=self.request.GET.get('page'))
        except PageNotAnInteger:
            screencasts = paginator.page(1)
        except EmptyPage:
            screencasts = paginator.page(paginator.num_pages)
        context.update(
            screencasts=screencasts,
            screencasts_filter=screencasts_filter,
        )
        return context


class ScreencastDetailView(ScreencastsBaseView):
    template_name = 'screencasts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sc = get_object_or_404(Screencast, slug=kwargs['slug'])
        # TODO прикрутить pygments
        sc.body = markdown(sc.body)
        context.update(sc=sc,)
        return context


class ScreencastsSearchView(ScreencastsBaseView):
    template_name = 'screencasts/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
