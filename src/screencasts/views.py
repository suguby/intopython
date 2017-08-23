# -*- coding: utf-8 -*-

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, CreateView

from src.articles.views import ArticlesBaseView
from src.payments.forms import PreOrderForm
from src.screencasts.forms import ScreencastForm
from .models import Screencast, ScreencastSection


class ScreencastsBaseView(ArticlesBaseView):
    model = Screencast
    list_url_name = 'screencasts'


class ScreencastsListView(ScreencastsBaseView):
    template_name = 'screencasts/index.html'
    PAGE_SIZE = 6

    def get_context_data(self, **kwargs):
        section_filter = self.request.GET.get('section')
        current_section = None
        if section_filter:
            self.articles_filter = Q(section__slug=section_filter)
            self.articles_url_filter = 'section={}&'.format(section_filter)
            current_section = get_object_or_404(ScreencastSection, slug=section_filter)
        sections = ScreencastSection.objects.filter(
            status=ScreencastSection.STATUSES.publ
        ).order_by('position')
        for section in sections:
            section.link = reverse('screencasts') + '?section={}'.format(section.slug)

        context = super().get_context_data(**kwargs)
        context.update(
            sections=sections,
            current_section=current_section,
        )
        return context


class ScreencastDetailView(ScreencastsBaseView):
    template_name = 'screencasts/detail.html'

    def get(self, request, *args, **kwargs):
        self.sc = get_object_or_404(Screencast, slug=kwargs['slug'])
        if isinstance(self.request.user, AnonymousUser):
            has_perm = not self.sc.by_subscription
        else:
            has_perm = self.request.user.has_perm(perm='view_subscription_article', obj=self.sc)
        if not has_perm:
            return HttpResponseRedirect(redirect_to=reverse('payments'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = dict(
            sc=self.sc,
            url_composer=self.url_composer,
            is_admin=self.user_is_admin(),
            tags=self.get_tags(),
        )
        return context


class ScreencastsSearchView(ArticlesBaseView):
    template_name = 'screencasts/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProVersionView(ScreencastsListView):
    template_name = 'screencasts/pro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PreOrderForm()
        return context


class ScreencastEditView(UpdateView, ScreencastsBaseView):
    template_name = 'screencasts/edit.html'
    form_class = ScreencastForm
    model = Screencast
    title = 'Редактирование скринкаста'

    def get(self, request, *args, **kwargs):
        if not self.user_is_admin():
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('screencast_edit', kwargs=dict(slug=kwargs.get('slug'))))
        self.object = get_object_or_404(self.model, slug=kwargs.get('slug'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=self.title,
        )
        return context

    def get_success_url(self):
        return reverse('screencast_detail', kwargs=dict(slug=self.kwargs.get('slug')))


class ScreencastCreateView(CreateView, ScreencastsBaseView):
    template_name = 'screencasts/edit.html'
    form_class = ScreencastForm
    model = Screencast
    title = 'Добавление скринкаста'

    def get(self, request, *args, **kwargs):
        if not self.user_is_admin():
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('screencast_add'))
        section = ScreencastSection.objects.first()
        self.object = Screencast(section=section)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=self.title,
        )
        return context

    def get_success_url(self):
        return reverse('screencasts')
