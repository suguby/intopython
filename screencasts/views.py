# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from screencasts.models import Screencast


class ScreencastsListView(TemplateView):
    template_name = 'screencasts/index.html'

    def get_context_data(self, **kwargs):
        screencasts = Screencast.objects.all()
        context = dict(
            screencasts=screencasts
        )
        return context