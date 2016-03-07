# -*- coding: utf-8 -*-
import datetime

from trans import trans


def get_translit(ustring):
    return trans(ustring.replace(' ', '-'))


def dt(src):
    u"""
        Преобразовать строку-дату в дату
    """
    if not issubclass(src.__class__, str):
        return src
    formats = ['%d-%m-%Y', '%d.%m.%Y', '%Y-%m-%d', '%Y.%m.%d', '%Y%m%d', ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(src, fmt).date()
        except ValueError:
            pass
    else:
        raise Exception("Date data '{text}' does not match any formats {formats}".format(text=src, formats=formats))


def limit_str(txt, limit=50):
    if len(txt) > limit:
        return txt[:limit] + '...'
    return txt
