#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class HttpRedirectException(Exception):

    def __init__(self, redirect_to):
        self.redirect_to = redirect_to


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(DEBUG=settings.DEBUG)
        return context

    def get(self, request, *args, **kwargs):
        self.request = request
        self.object = None  # костыль, что бы CreateView работал
        try:
            return super().get(request, *args, **kwargs)
        except HttpRedirectException as exc:
            return HttpResponseRedirect(redirect_to=exc.redirect_to)
