import django.test as unittest
import shutil
import os
import re

from ._adder import DefaultViewAdder
from ._api import Api
from ._utils import app_path
from ._utils import camel2under
from pprint import pprint


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

    def test_save_view_to_file(self):
        code = '''TestView(ListView):
    model = Book
    paginate_by = 10
'''
        shutil.copy2(
            os.path.join(app_path('test_app'), 'views.py'),
            os.path.join(app_path('test_app'), 'views.py.bac')
        )

        self.adder.save_view(code)
        f = open(os.path.join(app_path('test_app'), 'views.py'))
        file_text = f.read()
        f.close()

        shutil.copy2(
            os.path.join(app_path('test_app'), 'views.py.bac'),
            os.path.join(app_path('test_app'), 'views.py')
        )

        regexp = re.compile(r'.*{0}'.format(re.escape(code)), re.DOTALL)
        self.assertRegexpMatches(file_text, regexp)

    def test_camel2under(self):
        self.assertEqual(camel2under('MainProgramThread'), 'main_program_thread')

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
             'test_app/9.html', 'test_app/qqq.html', 'tpl1.html',
             'tpl2.html', 'asd/11.html', 'books/xyz.html']
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
            lines
        )
        self.assertEqual(lines[3], 'from test_app import TestView')

    def test_find_patterns(self):
        txt = '''urlpatterns = patterns('',
    url(r'^$', MainView.as_view(), name=MainView.url_name),
    url(r'^m/(?P<page>\d+)/$' , MainView.as_view(), name=MainView.url_name),
    url(r'^poczekalnia/$', PendingView.as_view(), name=PendingView.url_name),
)'''
        print self.adder._add_pattern(txt), 'xxx'










