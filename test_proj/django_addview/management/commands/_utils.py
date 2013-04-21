import re
from django.utils.importlib import import_module
from django.conf import settings

import_module(settings.ROOT_URLCONF)


def app_path(app_name):
    import_module(app_name)
    return  __import__(app_name).__path__[0]


def root_urlconf_path():
    return __import__(settings.ROOT_URLCONF).__path__[0]


def camel2under(txt):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', txt)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
