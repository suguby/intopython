# -*- coding: utf-8 -*-
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
        tags = Screencast.tags.all()
        context.update(
            sections=sections,
            tags=tags,
            blt=__builtins__,
        )
        return context


class ScreencastsListView(ScreencastsBaseView):
    template_name = 'screencasts/index.html'
    PAGE_SIZE = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sc_queryset = Screencast.objects.filter(
            status=Screencast.STATUSES.publ
        ).order_by('-created_at')
        section_filter = self.request.GET.get('section')
        filter_by_section = ''
        if section_filter:
            sc_queryset = sc_queryset.filter(section__slug=section_filter)
            filter_by_section += 'section={}&'.format(section_filter)
        paginator = Paginator(sc_queryset, self.PAGE_SIZE)
        try:
            screencasts = paginator.page(number=self.request.GET.get('page'))
        except PageNotAnInteger:
            screencasts = paginator.page(1)
        except EmptyPage:
            screencasts = paginator.page(paginator.num_pages)
        context.update(
            screencasts=screencasts,
            filter_by_section=filter_by_section,
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
