# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from screencasts.models import Screencast, ScreencastSection


class ScreencastsListView(TemplateView):
    template_name = 'screencasts/index.html'

    def get_context_data(self, **kwargs):

        screencasts = Screencast.objects.all().order_by('-created_at')
        section_filter = self.request.GET.get('section')
        if section_filter:
            screencasts = screencasts.filter(section__slug=section_filter)

        sections = ScreencastSection.objects.all().order_by('position')
        sections_split = len(sections)//2

        context = dict(
            screencasts=screencasts,
            sections=sections,
            sections_split=sections_split,
            blt=__builtins__,
        )
        return context