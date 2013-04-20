from ._config_loader import config, logger
from ._utils import app_path, camel2under
import os
import shutil

RESERVED_PARAMS = ('class_name')


class BaseViewAdder(object):

    def __init__(self, app_name, view_type, params):
        self.app_name = app_name
        self.view_type = view_type
        self.params = params

    def add_view(self):
        if self.view_type == 'function_view':
            self.add_function_view()
        else:
            self.add_cbv_view()

    def add_function_view(self, view_type, params):
        raise NotImplemented()

    def add_cbv_view(self):
        code = self.generate_cbv_view()
        self.save_view(code)
        self.create_template()
        self.update_url()
        self.add_test()

    def generate_cbv_view(self):
        raise NotImplementedError()

    def save_view(self, code):
        raise NotImplementedError()

    def create_template(self):
        raise NotImplementedError()

    def update_url(self):
        raise NotImplementedError()

    def add_test(self):
        raise NotImplementedError()


class DefaultViewAdder(BaseViewAdder):
    indent = '    '

    def generate_cbv_view(self):
        code = "class {class_name}({view_type}):\n".format(
            class_name=self.params['class_name'],
            view_type=self.view_type
        )

        for param_name, param_value in sorted(self.params.iteritems()):
            if param_name in RESERVED_PARAMS:
                continue
            code += "{indent}{param_name} = {param_value}\n".format(
                indent=self.indent,
                param_name=param_name,
                param_value=param_value
            )
        code += '\n'
        return code

    def save_view(self, code):
        view_file = open(
            os.path.join(app_path(self.app_name), 'views.py'),
            'a'
        )
        view_file.write('\n\n' + code)
        view_file.close()

    def create_template(self):
        create_from = self.params.get('template_create_from', None)
        if create_from is None:
            return

        tpl_dir = config['template_dir'].format(
            app_path=app_path(self.app_name),
            app_name=self.app_name
        )

        tpl_path = self.params.get('template_name', '')

        if not tpl_path:
            tpl_suffix = self.params.get('template_name_suffix', '')
            class_name = self.params.get('class_name')
            file_name = camel2under(class_name) + tpl_suffix + '.html'
            tpl_path = '{0}/{1}'.format(self.app_name, file_name)

        inner_dirs = tpl_path.split('/')[:-1]
        for i, _ in enumerate(inner_dirs):
            current_dir = os.path.join(tpl_dir, *inner_dirs[:i + 1])
            if not os.path.isdir(current_dir):
                os.mkdir(current_dir)

        if create_from is None:
            return
        elif create_from is '':
            open(os.path.join(tpl_dir, tpl_path), 'a').close()
        else:
            shutil.copy(
                os.path.join(tpl_dir, create_from),
                os.path.join(tpl_dir, tpl_path)
            )




