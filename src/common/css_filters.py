# -*- coding: utf-8 -*-
import re


def css_class(elem, klass):
    # TODO проверять есть ли уже class= и добавлять, может параметр сделать - заменять/добавлять
    # TODO и вообще сделать класс, там предкомпилить реджексы
    elem = str(elem)
    matched = re.search(r'^(\s*<\w+)\s*', elem)
    if not matched:
        return elem
    pos = matched.end(1)
    elem = u'{} class="{}" {}'.format(elem[:pos], klass, elem[pos:])
    return elem
