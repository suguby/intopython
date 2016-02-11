# -*- coding: utf-8 -*-

from src.common.views import BaseTemplateView


class CoursesView(BaseTemplateView):
    template_name = 'courses/index.html'


class CoursesProgramView(BaseTemplateView):
    template_name = 'courses/program.html'


class CoursesAuthorView(BaseTemplateView):
    template_name = 'courses/author.html'
