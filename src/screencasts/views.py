# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404

from src.articles.views import ArticlesBaseView
from src.common.views import HttpRedirectException, BaseTemplateView
from src.payments.forms import PreOrderForm
from src.payments.models import Tariff
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
        user = self.request.user
        context.update(
            sections=sections,
            current_section=current_section,
        )
        return context


class ScreencastDetailView(ScreencastsBaseView):
    template_name = 'screencasts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sc = get_object_or_404(Screencast, slug=kwargs['slug'])
        if isinstance(self.request.user, AnonymousUser):
            has_perm = not sc.by_subscription
        else:
            has_perm = self.request.user.has_perm(perm='view_subscription_article', obj=sc)
        if not has_perm:
            raise HttpRedirectException(redirect_to=reverse('payments'))
        context.update(sc=sc, )
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


class ScreencastEditView(ScreencastsBaseView):
    template_name = 'screencasts/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        if slug:
            sc = get_object_or_404(Screencast, slug=slug)
            form = ScreencastForm(instance=sc)
        else:
            form = ScreencastForm()
        context.update(
            form=form,
        )
        return context
