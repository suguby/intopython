from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView, CreateView

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

    def get(self, request, *args, **kwargs):
        if not self.user_is_admin():
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('blog_edit'))
        self.object = get_object_or_404(self.model, slug=kwargs.get('slug'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Редактирование записи блога'
        )
        return context

    def get_success_url(self):
        return reverse('blog_detail', kwargs=dict(slug=self.kwargs.get('slug')))


class BlogCreateView(CreateView, BlogBaseView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    model = Blog

    def get(self, request, *args, **kwargs):
        if not self.user_is_admin():
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('blog_add'))
        self.object = None
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title='Добавление записи блога'
        )
        return context

    def get_success_url(self):
        return reverse('blog')
