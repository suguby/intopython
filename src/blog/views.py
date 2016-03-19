from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from markdown import markdown

from src.articles.views import ArticlesBaseView
from .models import Blog


class BlogBaseView(ArticlesBaseView):
    model = Blog
    list_url_name = 'blog'
    PAGE_SIZE = 27


class BlogView(BlogBaseView):
    template_name = 'blog/index.html'


class BlogDetailView(BlogBaseView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Blog, slug=kwargs['slug'])
        article.body = markdown(article.body)
        context.update(article=article,)
        return context
