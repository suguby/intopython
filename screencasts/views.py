# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class ScreencastsListView(TemplateView):
    template_name = 'screencasts/index.html'
