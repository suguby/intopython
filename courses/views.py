from django.shortcuts import render
from django.views.generic import TemplateView


class CoursesView(TemplateView):
    template_name = 'courses/index.html'