# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from src.common.views import BaseTemplateView
from src.courses.forms import SignForm
from src.landing.models import LendingRegistration


class CoursesView(BaseTemplateView):
    template_name = 'courses/index.html'


class CoursesProgramView(BaseTemplateView):
    template_name = 'courses/program.html'


class CoursesAuthorView(BaseTemplateView):
    template_name = 'courses/author.html'


class CoursesSignView(BaseTemplateView):
    template_name = 'courses/sign.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SignForm()
        context.update(form=form)
        return context

    def post(self, request):
        form = SignForm(data=self.request.POST)
        context = dict(form=form)
        if form.is_valid():
            data = form.cleaned_data
            LendingRegistration.objects.get_or_create(
                email=data['email'], defaults=dict(name=data['name'], phone=data['phone']))
            message = (
                'Someone registered on lending: ',
                'email: '.format(data['email']),
                'name: '.format(data['name']),
                'phone: '.format(data['phone']),
            )
            mail.send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['itogo@mail.ru', ],
                subject='Lending registration',
                message='\n'.join(message),
            )
            return HttpResponseRedirect(reverse('courses_signed'))
        return self.render_to_response(context=context)


class CoursesSignedView(BaseTemplateView):
    template_name = 'courses/signed.html'
