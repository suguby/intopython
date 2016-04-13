# -*- coding: utf-8 -*-
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from src.registration.forms import MyUserCreationForm


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
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, user)
            return HttpResponseRedirect(redirect_to=form.cleaned_data['next'])
        context = dict(form=form)
        return self.render_to_response(context=context)


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request=request)
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)



class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        form = MyUserCreationForm()
        context = dict(form=form)
        return context
