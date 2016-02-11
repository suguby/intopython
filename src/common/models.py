# -*- coding: utf-8 -*-

from django.db import models


class AbstractModel(models.Model):
    _str_template = None  # fill with {attr1} {attr2}

    class Meta:
        abstract = True

    def __str__(self):
        class_name = self.__class__.__name__
        if self._str_template is None:
            return '{} / {}'.format(class_name, self.id)
        return '{}: {}'.format(class_name, self._str_template.format(**self.__dict__))
