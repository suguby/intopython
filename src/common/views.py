#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import TemplateView


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(DEBUG=settings.DEBUG)
        return context


class RegistrationView(TemplateView):
    template_name = 'registration/index.html'

    def get_context_data(self, **kwargs):
        form = UserCreationForm(data=self.request.POST)
        context = dict(form=form)
        return context

    def post(self, request, **kwargs):
        return self.render_to_response(context=self.get_context_data())
