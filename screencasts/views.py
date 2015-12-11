# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from markdown import markdown

from screencasts.models import Screencast, ScreencastSection


def fill_sidebar_context(context):
        sections = ScreencastSection.objects.annotate(
            count=Count('screencasts')
        ).filter(count__gt=0).order_by('position')
        sections_split = len(sections)//2
        context.update(
            sections=sections,
            sections_split=sections_split,
            blt=__builtins__,
        )


class ScreencastsListView(TemplateView):
    template_name = 'screencasts/index.html'

    def get_context_data(self, **kwargs):
        sc_queryset = Screencast.objects.all().order_by('-created_at')
        section_filter = self.request.GET.get('section')
        query_string = ''
        if section_filter:
            sc_queryset = sc_queryset.filter(section__slug=section_filter)
            query_string += 'section={}&'.format(section_filter)
        paginator = Paginator(sc_queryset, 2)
        try:
            screencasts = paginator.page(number=self.request.GET.get('page'))
        except PageNotAnInteger:
            screencasts = paginator.page(1)
        except EmptyPage:
            screencasts = paginator.page(paginator.num_pages)
        context = dict(
            screencasts=screencasts,
            query_string=query_string,
        )
        fill_sidebar_context(context)
        return context


class ScreencastDetailView(TemplateView):
    template_name = 'screencasts/detail.html'

    def get_context_data(self, **kwargs):
        sc = get_object_or_404(Screencast, slug=kwargs['slug'])
        sc.body = markdown(sc.body)
        context = dict(sc=sc,)
        fill_sidebar_context(context)
        return context
