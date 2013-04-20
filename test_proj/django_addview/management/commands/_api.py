import os
from ._config_loader import config, logger
from django.utils.importlib import import_module


class Api(object):

    def __init__(self):
        self.view_adder_cls = None

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
        template_dir = config['template_dir'].format(
            app_path=self.app_path,
            app_name=self.app_name
        )

        priority_files = []
        normal_files = []
        sub_files = []
        for path, _, files in os.walk(template_dir, topdown=True):
            subdirs = path[len(template_dir):].strip(os.path.sep)
            if len(subdirs) > 0:
                subdirs = subdirs.split(os.path.sep)
            else:
                subdirs = []

            if len(subdirs) > 0 and subdirs[0] == self.app_name:
                priority_files += \
                    [os.path.join(*(subdirs + [f])) for f in files]
            elif len(subdirs) > 0:
                sub_files += [os.path.join(*(subdirs + [f])) for f in files]
            else:
                normal_files += [os.path.join(*(subdirs + [f])) for f in files]
        return sorted(priority_files) + sorted(normal_files) + sorted(sub_files)

    def create_view(self, view_params):
        logger.warn('create_view')
        logger.warn(view_params)
        logger.warn(self.view_type)
