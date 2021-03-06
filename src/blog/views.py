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
        context = dict(
            article=article,
            url_composer=self.url_composer,
            is_admin=self.user_is_admin(),
            tags=self.get_tags(),
        )
        return context


class BlogEditView(UpdateView, BlogBaseView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    model = Blog
    title = 'Редактирование записи блога'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        if not self.user_is_admin():
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('blog_edit', kwargs=dict(slug=slug)))
        self.object = get_object_or_404(self.model, slug=slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=self.title
        )
        return context

    def get_success_url(self):
        return reverse('blog_detail', kwargs=dict(slug=self.kwargs.get('slug')))


class BlogCreateView(CreateView, BlogBaseView):
    template_name = 'blog/edit.html'
    form_class = BlogForm
    model = Blog
    title = 'Добавление записи блога'

    def get(self, request, *args, **kwargs):
        if not self.user_is_admin():
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('blog_add'))
        self.object = None
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=self.title
        )
        return context

    def get_success_url(self):
        return reverse('blog')
