# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import get_object_or_404
from markdown import markdown

from src.common.views import BaseTemplateView
from .models import Screencast, ScreencastSection


def fill_sidebar_context(context):
        sections = ScreencastSection.objects.all().order_by('position')
        sections_split = len(sections)//2
        context.update(
            sections=sections,
            sections_split=sections_split,
            blt=__builtins__,
        )


class ScreencastsListView(BaseTemplateView):
    template_name = 'screencasts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sc_queryset = Screencast.objects.filter(
            status=Screencast.STATUSES.publ
        ).order_by('-created_at')
        section_filter = self.request.GET.get('section')
        query_string = ''
        if section_filter:
            sc_queryset = sc_queryset.filter(section__slug=section_filter)
            query_string += 'section={}&'.format(section_filter)
        paginator = Paginator(sc_queryset, 27)
        try:
            screencasts = paginator.page(number=self.request.GET.get('page'))
        except PageNotAnInteger:
            screencasts = paginator.page(1)
        except EmptyPage:
            screencasts = paginator.page(paginator.num_pages)
        context.update(
            screencasts=screencasts,
            query_string=query_string,
        )
        fill_sidebar_context(context)
        return context


class ScreencastDetailView(BaseTemplateView):
    template_name = 'screencasts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        sc = get_object_or_404(Screencast, slug=kwargs['slug'])
        sc.body = markdown(sc.body)
        context.update(sc=sc,)
        fill_sidebar_context(context)
        return context


class ScreencastsSearchView(BaseTemplateView):
    template_name = 'screencasts/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        fill_sidebar_context(context)
        return context