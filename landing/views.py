# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, View

from landing.forms import RegisterForm


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        form = RegisterForm()
        context = dict(form=form)
        return context


class LandingRegisterView(View):

    def post(self):
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        phone = self.request.POST.get('phone')


