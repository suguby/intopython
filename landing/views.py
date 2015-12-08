# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, View


class LandingView(TemplateView):
    template_name = 'landing/index.html'


class LandingRegisterView(View):

    def post(self):
        email = self.request.POST.get('email')


