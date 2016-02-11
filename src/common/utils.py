# -*- coding: utf-8 -*-

from trans import trans


def get_translit(ustring):
    return trans(ustring.replace(' ', '-'))
