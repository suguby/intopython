# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, View

from landing.forms import RegisterForm
from landing.models import LendingRegistration


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        form = RegisterForm()
        context = dict(form=form)
        return context


class LandingRegisterView(View):

    def post(self):
        form = RegisterForm(self.request.POST)
        context = dict()
        if form.is_valid:
            user, created = LendingRegistration.objects.get_or_create(
                email=form.email, defaults=dict(name=form.name, phone=form.phone))
            context['created'] = created
        else:
            context.update(form=form)
        return render_to_response('', context=context)


