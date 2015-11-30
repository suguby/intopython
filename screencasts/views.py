# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from screencasts.models import Screencast, ScreencastSection


def fill_sidebar_context(context):
        sections = ScreencastSection.objects.filter(
            screencasts__isnull=False
        ).order_by('position')
        sections_split = len(sections)//2
        context.update(
            sections=sections,
            sections_split=sections_split,
            blt=__builtins__,
        )


class ScreencastsListView(TemplateView):
    template_name = 'screencasts/index.html'

    def get_context_data(self, **kwargs):

        screencasts = Screencast.objects.all().order_by('-created_at')
        section_filter = self.request.GET.get('section')
        if section_filter:
            screencasts = screencasts.filter(section__slug=section_filter)

        context = dict(
            screencasts=screencasts,
        )
        fill_sidebar_context(context)
        return context


class ScreencastDetailView(TemplateView):
    template_name = 'screencasts/detail.html'

    def get_context_data(self, **kwargs):
        sc = get_object_or_404(Screencast, slug=kwargs['slug'])
        context = dict(sc=sc,)
        fill_sidebar_context(context)
        return context
