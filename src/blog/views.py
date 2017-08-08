from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView

from src.articles.views import ArticlesBaseView
from src.blog.forms import BlogForm
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
        is_admin = False if isinstance(self.request.user, AnonymousUser) else self.request.user.is_admin
        context = dict(
            article=article,
            list_url_name=self.list_url_name,
            is_admin=is_admin,
        )
        return context


class BlogEditView(UpdateView, BlogBaseView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    model = Blog

    def get_object(self, queryset=None):
        pass

    def get_context_data(self, **kwargs):
        slug = kwargs.get('slug')
        if slug:
            self.object =get_object_or_404(Blog, slug=slug)
        else:
            self.object = Blog.objects.create()
        context = super().get_context_data(**kwargs)
        return context
