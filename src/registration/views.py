# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from src.payments.models import Orders
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
            redirect_to = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
            return HttpResponseRedirect(redirect_to=redirect_to)
        context = dict(form=form)
        return self.render_to_response(context=context)


class LogoutView(TemplateView):
    #  сразу переходим на next, без промежуточной страницы джанго

    def get(self, request, *args, **kwargs):
        logout(request=request)
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)


class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {}
        if not user.is_anonymous():
            if user.access_till > datetime.date.today():
                context.update(access_till=user.access_till)
            orders = Orders.objects.filter(user=user)
            context.update(orders=orders)
        return context
