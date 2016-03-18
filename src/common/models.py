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


# http://deliro.ru/posts/kak-rasshirit-model-user
# from django.contrib.auth.models import AbstractUser
# ROLES = (
#     (0, 'Foo'),
#     (1, 'Bar'),
# )
#
#
# class User(AbstractUser):
#     role = models.IntegerField(choices=ROLES)
#
#     class Meta(AbstractUser.Meta):
#         swappable = 'AUTH_USER_MODEL'
