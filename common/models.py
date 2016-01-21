# -*- coding: utf-8 -*-

from django.db import models


class AbstractModel(models.Model):
    _str_template = None  # fill with {attr1} {attr2}

    class Meta:
        abstract = True

    def __str__(self):
        if self._str_template is None:
            return '{} / {}'.format(self.__class__.__name__, self.id)
        return '{}: {}'.format(self.__class__.__name__, self._str_template.format(**self.__dict__))
