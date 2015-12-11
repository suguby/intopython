# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from landing.forms import RegisterForm
from landing.models import LendingRegistration


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        form = RegisterForm()
        context = dict(form=form)
        return context

    def post(self, request):
        form = RegisterForm(data=self.request.POST)
        context = dict(form=form)
        if form.is_valid():
            data = form.cleaned_data
            user, created = LendingRegistration.objects.get_or_create(
                email=data['email'], defaults=dict(name=data['name'], phone=data['phone']))
            context.update(show_thanks=True)
        else:
            context.update(show_register=True)
        return self.render_to_response(context=context)


