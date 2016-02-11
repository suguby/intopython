# -*- coding: utf-8 -*-
from inspect import isclass

from django.test import TestCase

from src.common import AbstractModel
from src.landing import models as land_models
from src.screencasts import models as sc_models


class AbstractTest(TestCase):

    def test_models_unicode(self):
        for mod in (sc_models, land_models, ):
            for name in dir(mod):
                if name.startswith('__') or name == 'AbstractModel':
                    continue
                klass = getattr(mod, name)
                if isclass(klass) and issubclass(klass, AbstractModel):
                    str(klass())

