from collections import Counter

from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from src.articles.models import Article
from src.common.views import BaseTemplateView


class ArticlesBaseView(BaseTemplateView):
    model = Article
    PAGE_SIZE = None
    articles_filter = Q()
    articles_url_filter = ''
    list_url_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = self.model.objects.filter(status=self.model.STATUSES.publ)

        # TODO уменьшить количество запросов
        slugs_counter = Counter((slug for sc in articles for slug in sc.tags.slugs()))
        tags = []
        if slugs_counter:
            count_range = slugs_counter.most_common(1)[0][1] / 4.0
            for tag in self.model.tags.order_by('name'):
                if tag.slug in slugs_counter:
                    tag.range = int(5 - slugs_counter[tag.slug] // count_range)
                    tags.append(tag)

        tag = self.request.GET.get('tag')
        if not self.articles_url_filter and tag:
            self.articles_filter = Q(tags__slug=tag)
            self.articles_url_filter = 'tag={}&'.format(tag)
        articles = articles.filter(
            self.articles_filter
        ).order_by('-created_at').prefetch_related('tagged_items__tag')

        if self.PAGE_SIZE:
            paginator = Paginator(articles, self.PAGE_SIZE)
            try:
                articles = paginator.page(number=self.request.GET.get('page'))
            except PageNotAnInteger:
                articles = paginator.page(1)
            except EmptyPage:
                articles = paginator.page(paginator.num_pages)

        for article in articles:
            if isinstance(self.request.user, AnonymousUser):
                article.user_can_view = not article.by_subscription
            else:
                article.user_can_view = self.request.user.has_perm(perm='view_subscription_article', obj=article)
        is_admin = False if isinstance(self.request.user, AnonymousUser) else self.request.user.is_admin
        context.update(
            articles=articles,
            tags=tags,
            url_filter=self.articles_url_filter,
            list_url_name=self.list_url_name,
            is_admin=is_admin,
        )
        return context
