# -*- coding: utf-8 -*-
from django.test import TestCase

from src.common.css_filters import add_css_class, replace_css_class


class TestLanding(TestCase):

    def test_add(self):
        self.assertEquals(add_css_class(
            '<input />', 'some_class'),
            '<input class="some_class" />')
        self.assertEquals(add_css_class(
            '<input class="class1" />', 'some_class'),
            '<input class="class1, some_class" />')
        self.assertEquals(add_css_class(
            '<input class="class1" />', 'some_class'),
            '<input class="class1, some_class" />')

    def test_replace(self):
        self.assertEquals(replace_css_class(
            '<input />', 'some_class'),
            '<input class="some_class" />')
        self.assertEquals(replace_css_class(
            '<input class="class1" />', 'some_class'),
            '<input class="some_class" />')

