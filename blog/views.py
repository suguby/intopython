from django.shortcuts import render
from django.views.generic import TemplateView

from blog.models import BlogRecord


class BlogView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        records = BlogRecord.objects.all()
        context = dict(records=records)
        return context
