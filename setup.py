# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup


version = __import__('django_addview').__version__

LONG_DESCRIPTION = """
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION


setup(name='django-addview',
      version=version,
      author='Jakub Kot',
      author_email='yakxxx@gmail.com',
      description='Adding views in Django as easy as pie.',
      license='BSD',
      keywords='django, view, views, scaffold, cbv, application',
      url='https://github.com/yakxxx/django-addview',
      packages=['django_addview',
                'django_addview.management',
                'django_addview.management.commands',
                'django_addview.management.commands.forms'],
      package_data={},
      long_description=long_description(),
      install_requires=['Django>=1.4.0',
                        'npyscreen>=2.0pre73'],
      classifiers=['Framework :: Django',
                   'Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Environment :: Console :: Curses',
                   'Programming Language :: Python :: 2.7'],
      zip_safe=False)
