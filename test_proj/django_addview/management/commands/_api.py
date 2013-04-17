import os
from _config_loader import config
from django.utils.importlib import import_module


class Api(object):
    def set_app_name(self, app_name):
        self.app_name = app_name
        import_module(app_name)
        self.app_path = __import__(app_name).__path__[0]
#        self.app_path =

    def get_template_filenames(self):
        template_dir = config['template_dir'].format(app_path=self.app_path)
        return os.listdir(template_dir)
