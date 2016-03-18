#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import EmailField
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(DEBUG=settings.DEBUG)
        return context


class MyUserCreationForm(UserCreationForm):
    email = EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ("username", )


class RegistrationView(TemplateView):
    template_name = 'registration/index.html'

    def get_context_data(self, **kwargs):
        form = MyUserCreationForm()
        context = dict(form=form)
        return context

    def post(self, request, **kwargs):
        form = MyUserCreationForm(data=self.request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            return HttpResponseRedirect(redirect_to=reverse('registration_success'))
        context = dict(form=form)
        return self.render_to_response(context=context)


class RegistrationSuccessView(TemplateView):
    template_name = 'registration/success.html'

