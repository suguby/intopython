# -*- coding: utf-8 -*-

from common.views import BaseTemplateView
from .models import LendingRegistration
from .forms import RegisterForm


class LandingView(BaseTemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        form = RegisterForm()
        context.update(form=form)
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


