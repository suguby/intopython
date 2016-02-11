#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(DEBUG=settings.DEBUG)
        return context