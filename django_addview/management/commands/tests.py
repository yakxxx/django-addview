import django.test as unittest
import shutil
import os
import re
from ._adder import DefaultViewAdder
from ._api import Api
from ._utils import app_path
from ._utils import camel2under
from ._config_loader import config
from pprint import pprint


class TestTemplateDirCreation(unittest.TestCase):
    def setUp(self):
        self.adder = DefaultViewAdder(
            'test_app',
            'DetailView',
            params={
                'class_name': 'Asd',
                'template_dir_choice': 'global',
                'template_create_from': ''
            }
        )
        os.rename(
            config['global_template_dir'],
            os.path.join(
                os.path.dirname(config['global_template_dir']),
                'template_bac'
            )
        )

    def tearDown(self):
        if os.path.isdir(config['global_template_dir']):
            shutil.rmtree(config['global_template_dir'])
        os.rename(
            os.path.join(
                os.path.dirname(config['global_template_dir']),
                'template_bac'
            ),
            config['global_template_dir']
        )

    def test_create_templates_dir(self):
        self.adder.create_template()
        self.assertTrue(os.path.isdir(config['global_template_dir']))
        self.assertTrue(os.path.isdir(
            os.path.join(config['global_template_dir'], 'test_app')
        ))


class TestTemplateCreation(unittest.TestCase):
    def test_create_empty_template(self):
        shutil.rmtree(
            os.path.join(app_path('test_app'), 'templates', 'books'),
            ignore_errors=True
        )
        adder2 = DefaultViewAdder(
            'test_app',
            'DetailView',
            {'template_name': 'books/xyz.html',
             'class_name': 'TestView',
             'model': 'Book',
             'template_create_from': ''
            })

        adder2.create_template()

        self.assertTrue(os.path.isdir(
            os.path.join(app_path('test_app'), 'templates', 'books'))
        )

        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    app_path('test_app'),
                    'templates',
                    'books',
                    'xyz.html'
                )
            )
        )

    def test_create_copy_template(self):
        shutil.rmtree(
            os.path.join(app_path('test_app'), 'templates', 'books'),
            ignore_errors=True
        )
        adder2 = DefaultViewAdder(
            'test_app',
            'DetailView',
            {'template_name': 'books/xyzaaa.html',
             'class_name': 'TestView',
             'model': 'Book',
             'template_create_from': 'tpl1.html'
            })

        adder2.create_template()

        self.assertTrue(os.path.isdir(
            os.path.join(app_path('test_app'), 'templates', 'books'))
        )

        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    app_path('test_app'),
                    'templates',
                    'books',
                    'xyzaaa.html'
                )
            )
        )

    def test_get_template_files(self):
        a = Api()
        a.set_app_name('test_app')
        a.get_template_filenames()
        self.assertListEqual(a.get_template_filenames(),
            ['test_app/0.html', 'test_app/1.html', 'test_app/2.html',
             'test_app/3.html', 'test_app/4.html', 'test_app/5.html',
             'test_app/6.html', 'test_app/7.html', 'test_app/8.html',
             'test_app/9.html', 'test_app/global1.html', 'test_app/qqq.html',
             'global0.html', 'tpl1.html', 'tpl2.html',
             'asd/11.html', 'books/xyz.html']
        )

    def test_get_models(self):
        a = Api()
        a.set_app_name('test_app')
        self.assertListEqual(
            a.get_model_names(),
            ['Book', 'Shelf']
        )


class TestViewCreation(unittest.TestCase):

    def setUp(self):
        shutil.copy2(
            os.path.join(app_path('test_app'), 'views.py'),
            os.path.join(app_path('test_app'), 'views.py.bac')
        )

        self.adder = DefaultViewAdder(
            'test_app',
            'DetailView',
            params={'paginate_by': 10,
             'class_name': 'TestView',
             'model': 'Book',
             'url_name': "'urlik'",
             'url_pattern': "r'^m/(?P<page>\d+)/$'"
            }
        )

    def tearDown(self):
        shutil.copy2(
            os.path.join(app_path('test_app'), 'views.py.bac'),
            os.path.join(app_path('test_app'), 'views.py')
        )

    def test_save_view_to_file(self):
        code = '''TestView(ListView):
    model = Book
    paginate_by = 10
'''
        self.adder.save_view(code)
        f = open(os.path.join(app_path('test_app'), 'views.py'))
        file_text = f.read()
        f.close()

        regexp = re.compile(r'.*{0}'.format(re.escape(code)), re.DOTALL)
        self.assertRegexpMatches(file_text, regexp)

    def test_update_import(self):
        self.adder.update_view_imports()
        f = open(os.path.join(app_path('test_app'), 'views.py'))
        file_text = f.read()
        f.close()

        reg = re.compile(
            r'from django.views.generic import DetailView',
            re.MULTILINE
        )
        self.assertRegexpMatches(file_text, reg)

        reg2 = re.compile(
            r'from test_app.models import Book',
            re.MULTILINE
        )
        self.assertRegexpMatches(file_text, reg2)

        self.adder.update_view_imports()
        self.adder.update_view_imports()
        self.adder.update_view_imports()

        f = open(os.path.join(app_path('test_app'), 'views.py'))
        file_text = f.read()
        f.close()

        self.assertEqual(len(re.findall(reg, file_text)), 1)
        self.assertEqual(len(re.findall(reg2, file_text)), 1)

    def test_is_imported(self):
        self.assertTrue(self.adder._is_imported(
            '\n\nfrom test_app.models import Book\n\n',
            'test_app.models',
            'Book'
        ))

    def test_update_existing_import(self):
        f = open(os.path.join(app_path('test_app'), 'views.py'), 'r+')
        cont = f.read()
        cont = 'from django.views.generic import *\n' + cont
        f.write(cont)
        f.close()

        self.adder.update_view_imports()
        f = open(os.path.join(app_path('test_app'), 'views.py'))
        file_text = f.read()
        f.close()

        reg = re.compile(
            r'from django.views.generic import DetailView',
            re.MULTILINE
        )
        self.assertFalse(reg.match(file_text))


class TestCodeGeneration(unittest.TestCase):
    def setUp(self):
        self.adder = DefaultViewAdder(
            'test_app',
            'DetailView',
            params={'paginate_by': 10,
             'class_name': 'TestView',
             'model': 'Book',
             'url_name': "'urlik'",
             'url_pattern': "r'^m/(?P<page>\d+)/$'"
            })

    def test_cbv_generation(self):
        code = self.adder.generate_cbv_view()

        self.assertRegexpMatches(code, r'TestView\(DetailView\):')
        self.assertRegexpMatches(code, r'paginate_by = 10')
        self.assertRegexpMatches(code, r'model = Book')

        #check indents
        for i, line in enumerate(code.split('\n')):
            if i == 0 or line == '':
                continue
            self.assertRegexpMatches(line, r' {4}')

    def test_camel2under(self):
        self.assertEqual(
            camel2under('MainProgramThread'), 'main_program_thread'
        )
        self.assertEqual(
            camel2under('ImportURLLib'),
            'import_url_lib'
        )

    def test_find_last_import_line(self):
        self.assertEqual(
            self.adder._find_last_import(
                ['from a import b', 'import abc', 'from x import *',
                 '', '', 'class Asd(object):', '    pass']
            ),
            2
        )

    def test_insert_import(self):
        lines = ['from a import b', 'import abc', 'from x import *', \
            '', '', 'class Asd(object):', '    pass']

        self.adder._insert_import(
            lines,
            _from='test_app.views',
            _import='TestView'
        )
        self.assertEqual(lines[3], 'from test_app.views import TestView')

    def test_find_patterns(self):
        txt = '''urlpatterns = patterns('',
    url(r'^$', MainView.as_view(), name=MainView.url_name),
    url(r'^m/(?P<page>\d+)/$' , MainView.as_view(), name=MainView.url_name),
    url(r'^poczekalnia/$', PendingView.as_view(), name=PendingView.url_name),
)'''
        self.assertEqual(
            self.adder._add_pattern(txt),
                '''urlpatterns = patterns('',
    url(r'^$', MainView.as_view(), name=MainView.url_name),
    url(r'^m/(?P<page>\d+)/$' , MainView.as_view(), name=MainView.url_name),
    url(r'^poczekalnia/$', PendingView.as_view(), name=PendingView.url_name),
    url(r'^m/(?P<page>\d+)/$', TestView.as_view(), name='urlik'),
)'''
        )

        #Same as above but params without trailing comma
        txt = txt[:-3] + txt[-2:]

        self.assertEqual(
            self.adder._add_pattern(txt),
                '''urlpatterns = patterns('',
    url(r'^$', MainView.as_view(), name=MainView.url_name),
    url(r'^m/(?P<page>\d+)/$' , MainView.as_view(), name=MainView.url_name),
    url(r'^poczekalnia/$', PendingView.as_view(), name=PendingView.url_name),
    url(r'^m/(?P<page>\d+)/$', TestView.as_view(), name='urlik'),
)'''
        )

        #One liner
        txt2 = ('''urlpatterns = patterns('','''
                '''url(r'^$', MainView.as_view(), name=MainView.url_name),)''')

        self.assertEqual(
            self.adder._add_pattern(txt2),
            '''urlpatterns = patterns('',\
url(r'^$', MainView.as_view(), name=MainView.url_name),
    url(r'^m/(?P<page>\d+)/$', TestView.as_view(), name='urlik'),
)'''
        )
