# -*- coding: utf-8 -*-
import re


class CssChanger:

    def __init__(self):
        self._re_tag_begin = re.compile(r'^(\s*<\w+)\s+')
        self._re_css_class = re.compile(r'\s+class="(.*?)"\s*')

    def add(self, matched, elem, klass):
        pos = matched.end(1)
        elem = '{}, {}{}'.format(elem[:pos], klass, elem[pos:])
        return elem

    def replace(self, matched, elem, klass):
        elem = '{}{}{}'.format(elem[:matched.start(1)], klass, elem[matched.end(1):])
        return elem

    def do(self, elem, klass, action):
        elem = str(elem)
        matched = self._re_css_class.search(elem)
        if matched:
            return action(matched, elem, klass)
        else:
            matched = self._re_tag_begin.search(elem)
            if not matched:
                return elem
            pos = matched.end(1)
            elem = u'{} class="{}"{}'.format(elem[:pos], klass, elem[pos:])
            return elem

_css_changer = CssChanger()


def add_css_class(elem, klass):
    """
        Add given klass to existing tag class definition
        class='cls1, cls2' -> class='cls1, cls2, klass'
    """
    return _css_changer.do(elem, klass, _css_changer.add)


def set_css_class(elem, klass):
    """
        Whole replace tag class definition with given klass
        class='cls1, cls2, ...' -> class='klass'
    """
    return _css_changer.do(elem, klass, _css_changer.replace)
