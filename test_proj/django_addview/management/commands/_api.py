import os
from _config_loader import config, logger
from django.utils.importlib import import_module


class Api(object):
    def set_app_name(self, app_name):
        self.app_name = app_name
        import_module(app_name)
        self.app_path = __import__(app_name).__path__[0]
#        self.app_path =

    def get_app_path(self):
        assert(
            getattr(self, 'app_path'),
            'You have to invoke set_app_name() before'
        )
        return self.app_path

    def set_view_type(self, view_type_name):
        self.view_type = view_type_name

    def get_template_filenames(self):
        assert(
            getattr(self, 'app_path'),
            'You have to invoke set_app_name() before'
        )
        template_dir = config['template_dir'].format(app_path=self.app_path)
        return os.listdir(template_dir)

    def create_view(self, view_params):
        logger.warn('create_view')
        logger.warn(view_params)
        logger.warn(self.view_type)
