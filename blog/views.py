from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from markdown import markdown

from blog.models import Blog


class BlogView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flt = dict(status=Blog.STATUSES.publ)
        tag = self.request.GET.get('tag')
        if tag:
            flt.update(tags__slug=tag)
        sc_queryset = Blog.objects.filter(**flt).order_by('-created_at')
        section_filter = self.request.GET.get('section')
        query_string = ''
        if section_filter:
            sc_queryset = sc_queryset.filter(section__slug=section_filter)
            query_string += 'section={}&'.format(section_filter)
        paginator = Paginator(sc_queryset, 2)
        try:
            articles = paginator.page(number=self.request.GET.get('page'))
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        tags = {}
        for bl in Blog.objects.filter(status=Blog.STATUSES.publ).prefetch_related('tags'):
            for tag in bl.tags.all():
                tags[tag.slug] = tag.name

        context.update(
            articles=articles,
            query_string=query_string,
            tags=tags,
        )
        return context


class BlogDetailView(TemplateView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        article = get_object_or_404(Blog, slug=kwargs['slug'])
        article.body = markdown(article.body)
        context.update(article=article,)
        return context
