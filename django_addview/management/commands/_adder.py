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
        logger.debug('ADD VIEW:')
        logger.debug(self.view_type)
        logger.debug(self.params)
        if self.view_type == 'function_view':
            self.add_function_view()
        else:
            self.add_cbv_view()

    def add_function_view(self):
        code = self.generate_function_view()
        self.save_view(code)
        self.update_view_imports(
            'django.shortcuts',
            'render'
        )
        self.create_template()
        self.update_urls()
        code = self.generate_test()
        self.add_test(code)

    def add_cbv_view(self):
        code = self.generate_cbv_view()
        self.save_view(code)
        self.update_view_imports(
            'django.views.generic',
             self.view_type
        )
        self.create_template()
        self.update_urls()
        code = self.generate_test()
        self.add_test(code)

    def generate_cbv_view(self):
        raise NotImplementedError()

    def generate_function_view(self):
        raise NotImplementedError()

    def save_view(self, code):
        raise NotImplementedError()

    def create_template(self):
        raise NotImplementedError()

    def update_urls(self):
        raise NotImplementedError()

    def generate_test(self):
        raise NotImplementedError()

    def add_test(self, code):
        raise NotImplementedError()


class DefaultViewAdder(BaseViewAdder):
    indent = '    '

    def generate_function_view(self):
        code = "def {function_name}(request):\n".format(
            function_name=self.params['function_name']
        )
        code += "{indent}return render(request, '{tpl}')\n".format(
            indent=self.indent,
            tpl=self.select_template_name()
        )
        return code

    def generate_cbv_view(self):
        code = "class {class_name}({view_type}):\n".format(
            class_name=self.params['class_name'],
            view_type=self.view_type
        )

        at_least_one_line = False
        for param_name, param_value in sorted(self.params.iteritems()):
            if param_name in RESERVED_PARAMS or param_value == '':
                continue
            at_least_one_line = True
            code += "{indent}{param_name} = {param_value}\n".format(
                indent=self.indent,
                param_name=param_name,
                param_value=param_value
            )

        if not at_least_one_line:
            code += "{indent}pass\n".format(indent=self.indent)

        code += '\n'
        return code

    def save_view(self, code):
        try:
            view_file = open(
                os.path.join(app_path(self.app_name), 'views.py'),
                'a'
            )
            view_file.write('\n' + code)
            view_file.close()
        except IOError:
            logger.error('Couldn\'t open {0}. View code not added'.format(
                os.path.join(app_path(self.app_name), 'views.py')
            ))
            return

    def update_view_imports(self, _from, _import):
        try:
            view_file = open(
                os.path.join(app_path(self.app_name), 'views.py'),
                'r'
            )
            view_content = view_file.read()
            view_file.close()
        except IOError:
            logger.error('Couldn\'t open {0}. Imports not added'.format(
                os.path.join(app_path(self.app_name), 'views.py')
            ))
            return

        lines = view_content.split('\n')

        self._insert_import(lines, _from, _import)

        if self.params.get('model', None):
            self._insert_import(
                lines,
                _from='{0}.models'.format(self.app_name),
                _import=self.params['model']
            )

        try:
            view_file = open(
                os.path.join(app_path(self.app_name), 'views.py'),
                'w'
            )
            view_file.write('\n'.join(lines))
            view_file.close()
        except IOError:
            logger.error(
                'Couldn\'t open {0} for writing. Imports not added'.format(
                    os.path.join(app_path(self.app_name), 'views.py')
                )
            )

    def create_template(self):
        create_from = self.params.get('template_create_from', None)
        if create_from is None:
            return

        tpl_dir = self._select_template_dir()
        if not tpl_dir:
            logger.error(
                'No tpl dir set:{0}. Template not created.'.format(tpl_dir)
            )
            return

        if not os.path.isdir(tpl_dir):
            try:
                os.mkdir(tpl_dir)
            except:
                logger.error(
                    "Couldn't create dir: {0}."
                    " Template not created".format(tpl_dir)
                )

        tpl_path = self.select_template_name()

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

    def select_template_name(self):
        tpl_path = self.params.get('template_name', '').strip("`'\"")
        if not tpl_path:
            tpl_suffix = self.params.get('template_name_suffix', '')
            tpl_suffix = tpl_suffix.strip("`'\"")
            class_name = self.params.get('class_name', None)
            function_name = self.params.get('function_name', None)

            if class_name:
                file_name = camel2under(class_name) + tpl_suffix + '.html'
            elif function_name:
                file_name = camel2under(function_name) + '.html'
            else:
                logger.error("No file_name nor class_name provided")
                assert False, "It shoudln't happen"

            tpl_path = '{0}/{1}'.format(self.app_name, file_name)
        return tpl_path

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
        self._insert_import(
            urls_lines,
            '{0}.views'.format(self.app_name),
             self.params.get('class_name', None) or \
                    self.params.get('function_name')
        )
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

    def _insert_import(self, lines, _from, _import):
        import_text = 'from {0} import {1}'.format(
            _from,
            _import
        )

        if self._is_imported(
            '\n'.join(lines),
            _from,
            _import
        ):
            return

        last_import_line = self._find_last_import(lines)
        lines.insert(last_import_line + 1, import_text)

    def _is_imported(self, view_content, _from, _import):
        regs = [
            r'import\s*{0}'.format(re.escape(_import)),
            r'from {0}\s*import\s*\*'.format(re.escape(_from))
        ]
        if any([re.search(reg, view_content) for reg in regs]):
            return True
        else:
            return False

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

        if self.params.get('class_name', None):
            appendix = '.as_view()'
        else:
            appendix = ''

        if self.params.get('url_name', None):
            tpl = ('url({regexp}, {name}{appendix}'
                ', name={url_name}),\n')
        else:
            tpl = 'url({regexp}, {name}{appendix}),\n'

        params += \
            tpl.format(
                regexp=self.params.get('url_pattern', ''),
                name=self.params.get('class_name', None) or\
                            self.params.get('function_name'),
                url_name=self.params.get('url_name', ''),
                appendix=appendix,
            )

        return re.sub(
            r'(.*urlpatterns\s*=\s*patterns\()(.*)(\))',
            r'\1{0}\3'.format(params),
            urls_content,
            flags=re.DOTALL
        )
