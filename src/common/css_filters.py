# -*- coding: utf-8 -*-
import re


def css_class(elem, klass):
    elem = str(elem)
    matched = re.search(r'^(\s*<\w+)\s*', elem)
    if not matched:
        return elem
    pos = matched.end(1)
    elem = u'{} class="{}" {}'.format(elem[:pos], klass, elem[pos:])
    return elem
