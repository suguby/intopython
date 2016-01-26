
from django.views.generic import TemplateView


class BlogView(TemplateView):
    template_name = 'blog/index.html'


class BlogDetailView(TemplateView):
    template_name = 'blog/detail.html'

