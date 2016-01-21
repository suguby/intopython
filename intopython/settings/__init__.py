# -*- coding: utf-8 -*-
import sys

from .base import *

try:
    from .local import *
except ImportError:
    print("Can't find module settings.local! Make it from local.py.skeleton")

#if manage.py test was called, use test settings
if 'test' in sys.argv or 'jenkins' in sys.argv:
    try:
        from .testing import *
    except ImportError:
        pass
