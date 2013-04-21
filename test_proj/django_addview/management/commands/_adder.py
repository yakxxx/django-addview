from ._config_loader import config, logger
from ._utils import app_path, camel2under, root_urlconf_path
import os
import re
import shutil

RESERVED_PARAMS = (
    'class_name',
    'template_create_from',
    'template_dir_choice',
    'urls_to_edit',
    'url_pattern',
    'url_name',
)


class BaseViewAdder(object):

    def __init__(self, app_name=None, view_type=None, params=None):
        assert(app_name is not None)
        assert(view_type is not None)
        assert(params is not None)

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
        self.update_urls()
        code = self.generate_test()
        self.add_test(code)

    def generate_cbv_view(self):
        raise NotImplementedError()

    def save_view(self, code):
        raise NotImplementedError()

    def create_template(self):
        raise NotImplementedError()

    def update_url(self):
        raise NotImplementedError()

    def generate_test(self):
        raise NotImplementedError()

    def add_test(self, code):
        raise NotImplementedError()


class DefaultViewAdder(BaseViewAdder):
    indent = '    '

    def generate_cbv_view(self):
        code = "class {class_name}({view_type}):\n".format(
            class_name=self.params['class_name'],
            view_type=self.view_type
        )

        for param_name, param_value in sorted(self.params.iteritems()):
            if param_name in RESERVED_PARAMS or param_value == '':
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

        tpl_dir = self._select_template_dir()
        if not tpl_dir:
            logger.error('No tpl dir set. Template not created.')
            return
        if not os.path.isdir(tpl_dir):
            try:
                os.mkdir(tpl_dir)
            except:
                logger.error(
                    "Couldn't create dir: {0}."
                    " Template not created".format(tpl_dir)
                )

        tpl_path = self.params.get('template_name', '')

        if not tpl_path:
            tpl_suffix = self.params.get('template_name_suffix', '')
            class_name = self.params.get('class_name')
            file_name = camel2under(class_name) + tpl_suffix + '.html'
            tpl_path = '{0}/{1}'.format(self.app_name, file_name)

        self._create_dirs_on_path(tpl_dir, tpl_path)

        if create_from is '':
            open(os.path.join(tpl_dir, tpl_path), 'a').close()
        else:
            shutil.copy(
                os.path.join(tpl_dir, create_from),
                os.path.join(tpl_dir, tpl_path)
            )

    def _select_template_dir(self):
        tpl_dir_choice = self.params.get('template_dir_choice', 'local')
        if tpl_dir_choice == 'global':
            tpl_dir = config['global_template_dir']
        else:
            tpl_dir = config['local_template_dir'].format(
                app_path=app_path(self.app_name),
                app_name=self.app_name
            )
        return tpl_dir

    def _create_dirs_on_path(self, main_dir, path):
        inner_dirs = path.split('/')[:-1]
        for i, _ in enumerate(inner_dirs):
            current_dir = os.path.join(main_dir, *inner_dirs[:i + 1])
            if not os.path.isdir(current_dir):
                os.mkdir(current_dir)

    def generate_test(self):
        pass

    def add_test(self, code):
        pass

    def update_urls(self):
        urls_to_edit = self.params.get('urls_to_edit', None)
        if urls_to_edit == 'global':
            urls_path = os.path.join(root_urlconf_path(), 'urls.py')
        elif urls_to_edit == 'local':
            urls_path = os.path.join(app_path(self.app_name), 'urls.py')
        else:
            return

        logger.debug(urls_path)
        try:
            f = open(urls_path, 'r')
            urls_content = f.read()
            f.close()
        except IOError:
            logger.error(
                'Couldn\'t open file {0} for read. '
                'No entry added to URLconf'.format(urls_path)
            )
            return

        urls_lines = urls_content.split('\n')
        self._insert_import(urls_lines)
        urls_content = "\n".join(urls_lines)
        urls_content = self._add_pattern(urls_content)

        try:
            f = open(urls_path, 'w')
            f.write(urls_content)
            f.close()
        except IOError:
            logger.error(
                'Couldn\'t open file {0} for write. '
                'No entry added to URLconf'.format(urls_path)
            )
            return

    def _insert_import(self, lines):
        import_text = 'from {app}.views import {cls}'.format(
            app=self.app_name,
            cls=self.params.get('class_name')
        )
        last_import_line = self._find_last_import(lines)
        lines.insert(last_import_line + 1, import_text)

    def _find_last_import(self, lines):
        last_import_line = -1
        for i, line in enumerate(lines):
            if re.match('[^#]*import.*', line):
                last_import_line = i
        return last_import_line

    def _add_pattern(self, urls_content):
        m = re.match(
            r'.*urlpatterns\s*=\s*patterns\((?P<params>.*)\)',
            urls_content,
            re.DOTALL
        )
        params = m.group('params').strip()
        if params[len(params) - 1] != ',':
            params += ','
        params += '\n{indent}'.format(indent=self.indent)
        params += \
            ('url({regexp}, {class_name}.as_view()'
            ', name={url_name}),\n').format(
                regexp=self.params.get('url_pattern'),
                class_name=self.params.get('class_name'),
                url_name=self.params.get('url_name')
            )

        return re.sub(
            r'(.*urlpatterns\s*=\s*patterns\()(.*)(\))',
            r'\1{0}\3'.format(params),
            urls_content,
            flags=re.DOTALL
        )

