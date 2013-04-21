import re
from django.utils.importlib import import_module
from django.conf import settings


def app_path(app_name):
    import_module(app_name)
    return  __import__(app_name).__path__[0]


def root_urlconf_path():
    import_module(settings.ROOT_URLCONF)
    return __import__(settings.ROOT_URLCONF).__path__[0]


def camel2under(txt):
    return re.sub(r'([A-Z])([a-z0-9])', r'_\1\2', txt).lower().strip('_')
