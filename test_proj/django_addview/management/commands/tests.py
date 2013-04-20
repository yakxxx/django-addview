import django.test as unittest
import shutil
import os
import re

from ._utils import app_path
from ._adder import DefaultViewAdder
from ._utils import camel2under
from pprint import pprint


class TestCodeGeneration(unittest.TestCase):
    def setUp(self):
        self.adder = DefaultViewAdder(
            'test_app',
            'DetailView',
            {'paginate_by': 10,
             'class_name': 'TestView',
             'model': 'Book'
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

    def test_create_template(self):
        adder2 = DefaultViewAdder(
            'test_app',
            'DetailView',
            {'template_name': 'books/xyz.html',
             'class_name': 'TestView',
             'model': 'Book'
            })

        adder2.create_template()


