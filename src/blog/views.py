from django.shortcuts import get_object_or_404

from src.articles.views import ArticlesBaseView
from .models import Blog


class BlogBaseView(ArticlesBaseView):
    model = Blog
    list_url_name = 'blog'


class BlogView(BlogBaseView):
    template_name = 'blog/index.html'
    PAGE_SIZE = 7


class BlogDetailView(BlogBaseView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        article = get_object_or_404(Blog, slug=kwargs['slug'])
        context = dict(
            article=article,
            list_url_name=self.list_url_name,
        )
        return context
