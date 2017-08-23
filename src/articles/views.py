from collections import Counter

from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.urls import reverse

from src.articles.models import Article
from src.common.views import BaseTemplateView


class UrlComposer:

    def __init__(self, list_url_name, params):
        self.list_url_name = list_url_name
        self.params = params
        self.clear = False
        self.tags = {}

    def get_list_url(self, clear=False, **tags):
        return self.get_url(uri=reverse(self.list_url_name), clear=clear, **tags)

    def get_url(self, uri, clear=False, **tags):
        self.clear = clear
        self.tags = tags
        return self._get_query(uri=uri)

    def _get_query(self, uri):
        _flt = self._get_filter()
        if _flt:
            return uri + '?{}'.format('&'.join(['{}={}'.format(k, v) for k, v in _flt.items()]))
        return uri

    def _get_filter(self):
        _flt = {}
        if not self.clear:
            for param in ('page', 'tag'):
                if param in self.params:
                    _flt[param] = self.params[param]
        for tag, value in self.tags.items():
            _flt[tag] = value
        return _flt


class ArticlesBaseView(BaseTemplateView):
    model = Article
    PAGE_SIZE = None
    articles_url_filter = ''
    list_url_name = 'articles'

    def __init__(self):
        self._articles = None
        super(ArticlesBaseView, self).__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            articles=self.get_filtered_articles(),
            tags=self.get_tags(),
            is_admin=self.user_is_admin(),
            url_composer=self.url_composer,
        )
        return context

    @property
    def articles(self):
        if self._articles:
            return self._articles
        self._articles = self.model.objects.filter(
            status=self.model.STATUSES.publ
        ).order_by('-created_at').prefetch_related('tagged_items__tag')
        for article in self._articles:
            if isinstance(self.request.user, AnonymousUser):
                article.user_can_view = not article.by_subscription
            else:
                article.user_can_view = self.request.user.has_perm(perm='view_subscription_article', obj=article)
        return self._articles

    @property
    def url_composer(self):
        return UrlComposer(list_url_name=self.list_url_name, params=self.request.GET)

    def get_filtered_articles(self):
        filtered_articles = self.articles
        tag = self.request.GET.get('tag')
        if tag:
            filtered_articles = self._articles.filter(Q(tags__slug=tag))
        if self.PAGE_SIZE:
            paginator = Paginator(filtered_articles, self.PAGE_SIZE)
            try:
                filtered_articles = paginator.page(number=self.request.GET.get('page'))
            except PageNotAnInteger:
                filtered_articles = paginator.page(1)
            except EmptyPage:
                filtered_articles = paginator.page(paginator.num_pages)
        return filtered_articles

    def get_tags(self):
        # TODO уменьшить количество запросов
        slugs_counter = Counter((slug for sc in self.articles for slug in sc.tags.slugs()))
        tags = []
        if slugs_counter:
            count_range = slugs_counter.most_common(1)[0][1] / 4.0
            for tag in self.model.tags.order_by('name'):
                if tag.slug in slugs_counter:
                    tag.range = int(5 - slugs_counter[tag.slug] // count_range)
                    tags.append(tag)
        return tags

    def user_is_admin(self):
        return False if isinstance(self.request.user, AnonymousUser) else self.request.user.is_admin
