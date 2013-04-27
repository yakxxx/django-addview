import os
import re
from django.utils.importlib import import_module
from ._adder import DefaultViewAdder
from ._config_loader import config, logger


class Api(object):

    def __init__(self):
        self.view_params = {}
        self.view_adder_cls = DefaultViewAdder

    def set_app_name(self, app_name):
        self.app_name = app_name
        import_module(app_name)
        self.app_path = __import__(app_name).__path__[0]
#        self.app_path =

    def get_app_path(self):
        assert hasattr(self, 'app_path'), \
            'You have to invoke set_app_name() before'

        return self.app_path

    def set_view_type(self, view_type_name):
        self.view_type = view_type_name

    def get_model_names(self):
        model_path = os.path.join(self.get_app_path(), 'models.py')
        if not os.path.isfile(model_path):
            return []

        try:
            f = open(model_path, 'r')
            models = f.read()
            f.close()
        except IOError:
            logger.error('Couln\'t open {0}.'.format(model_path))
            return []

        return [m.group(1) for m in re.finditer(
            '\s*class (.*?)\(.*?\):',
            models,
            re.MULTILINE
        )]

    def get_template_name(self):
        view_adder = self.view_adder_cls(
            app_name=self.app_name,
            view_type=self.view_type,
            params=self.view_params
        )
        logger.warn(self.view_params)
        return view_adder.select_template_name()

    def get_template_filenames(self):
        assert hasattr(self, 'app_path'), \
            'You have to invoke set_app_name() before'

        local_template_dir = config['local_template_dir'].format(
            app_path=self.app_path,
            app_name=self.app_name
        )
        global_template_dir = config['global_template_dir']

        local_templates = self._get_template_filenames_from_dir(
            local_template_dir
        )
        global_templates = self._get_template_filenames_from_dir(
            global_template_dir
        )
        ret = []
        for i in xrange(3):
            ret += sorted(local_templates[i] + global_templates[i])
        return ret

    def _get_template_filenames_from_dir(self, template_dir):
        if not template_dir:
            return [], [], []

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
        return (sorted(priority_files), sorted(normal_files), \
                    sorted(sub_files))

    def update_view_params(self, view_params):
        self.view_params.update(view_params)
        logger.debug('create_view')
        logger.debug(view_params)
        logger.debug(self.view_type)

    def add_view(self):
        view_adder = self.view_adder_cls(
            app_name=self.app_name,
            view_type=self.view_type,
            params=self.view_params
        )
        view_adder.add_view()

API = Api()
