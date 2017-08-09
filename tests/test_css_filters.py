# -*- coding: utf-8 -*-
from django.test import TestCase

from src.common.css_filters import add_css_class, set_css_class


class TestCssFilter(TestCase):

    def test_add(self):
        self.assertEquals(add_css_class(
            '<input />', 'some_class'),
            '<input class="some_class" />')
        self.assertEquals(add_css_class(
            '<input class="class1" />', 'some_class'),
            '<input class="class1 some_class" />')
        self.assertEquals(add_css_class(
            '<input class="class1 class2" />', 'some_class'),
            '<input class="class1 class2 some_class" />')
        self.assertEquals(add_css_class(
            'some_string', 'some_class'),
            'some_string')

    def test_replace(self):
        self.assertEquals(set_css_class(
            '<input />', 'some_class'),
            '<input class="some_class" />')
        self.assertEquals(set_css_class(
            '<input class="class1" />', 'some_class'),
            '<input class="some_class" />')
        self.assertEquals(set_css_class(
            '<input class="class1 class2" />', 'some_class'),
            '<input class="some_class" />')
        self.assertEquals(set_css_class(
            'some_string', 'some_class'),
            'some_string')
