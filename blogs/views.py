from django.shortcuts import render
from django.views.generic import TemplateView

from blogs.models import BlogRecord


class BlogsView(TemplateView):
    template_name = 'blogs/index.html'

    def get_context_data(self, **kwargs):
        recs = BlogRecord.objects.all()
        context = dict(
            mess='Привет!',
            recs=recs,
        )
        return context
