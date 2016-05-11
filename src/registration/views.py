# -*- coding: utf-8 -*-
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from src.registration.forms import MyUserCreationForm
from src.registration.models import MyUser


class RegistrationView(TemplateView):
    template_name = 'registration/index.html'

    def get_context_data(self, **kwargs):
        form = MyUserCreationForm()
        context = dict(form=form)
        return context

    def post(self, request, **kwargs):
        form = MyUserCreationForm(data=self.request.POST)
        if form.is_valid():
            MyUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            login(request, user)
            redirect_to = request.GET.get('next', '/')
            return HttpResponseRedirect(redirect_to=redirect_to)
        context = dict(form=form)
        return self.render_to_response(context=context)


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request=request)
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)


class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        form = MyUserCreationForm()
        context = dict(form=form)
        return context
