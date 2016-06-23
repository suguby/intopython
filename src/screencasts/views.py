# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from src.articles.views import ArticlesBaseView
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(sc=self.request.sc, )
        return context

    def get(self, request, *args, **kwargs):
        sc = get_object_or_404(Screencast, slug=kwargs['slug'])
        if isinstance(self.request.user, AnonymousUser):
            has_perm = not sc.by_subscription
        else:
            has_perm = self.request.user.has_perm(perm='view_subscription_article', obj=sc)
        if not has_perm:
            return HttpResponseRedirect(redirect_to=reverse('order'))
        request.sc = sc
        return super(ScreencastDetailView, self).get(request, *args, **kwargs)


class ScreencastsSearchView(ArticlesBaseView):
    template_name = 'screencasts/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
