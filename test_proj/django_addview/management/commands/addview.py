from django.core.management.base import BaseCommand
import npyscreen
import logging

from _api import Api
logger = logging.getLogger('addview')
hdlr = logging.FileHandler('addview.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

API = Api()


class TemplateFormMixin(object):

    def create(self):
        self.template_name = self.add(npyscreen.TitleText, name='template_name')

        choices = \
            ['Create empty', 'Don\'t create'] + \
            ['copy {0}'.format(file_name)
              for file_name in sorted(API.get_template_filenames())]
        self.template_creation = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=7,
            name='Create template from:',
            values=choices
        )


class ViewParamsForm(npyscreen.Form, TemplateFormMixin):
    def create(self):
        self.myName = self.add(npyscreen.TitleText, name='Name')
        TemplateFormMixin.create(self)


class DetailViewParamsForm(npyscreen.Form, TemplateFormMixin):
    def create(self):
        self.model = self.add(npyscreen.TitleText, name='model')
        TemplateFormMixin.create(self)


class TemplateViewParamsForm(npyscreen.Form, TemplateFormMixin):
    def create(self):
        TemplateFormMixin.create(self)


class ListViewParamsForm(npyscreen.Form):
    def create(self):
        self.template_name = self.add(npyscreen.TitleText, name='template_name')
        self.model = self.add(npyscreen.TitleText, name='model')


class FunctionViewParamsForm(npyscreen.Form):
    def create(self):
        self.myName = self.add(npyscreen.TitleText, name='Name')


class ViewTypeForm(npyscreen.Form):
    next_view = {
        'View': 'ViewParamsForm',
        'DetailView': 'DetailViewParamsForm',
        'TemplateView': 'TemplateViewParamsForm',
        'ListView': 'ListViewParamsForm',
        'function_view': 'FunctionViewParamsForm'
    }
    choices = ['View', 'DetailView', 'TemplateView',
                'ListView', 'function_view'
              ]

    def create(self):
        self.view_type = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=7,
            name='View Type',
            values=self.choices
        )

    def afterEditing(self):
        try:
            value = self.view_type.value[0]
        except IndexError:
            value = None

        choice = self.choices[value]

        self.parentApp.NEXT_ACTIVE_FORM = self.next_view.get(
            choice,
            None
        )
        logger.warn(self.parentApp.NEXT_ACTIVE_FORM)


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', ViewTypeForm, name='View Type')
        self.addForm('ViewParamsForm', ViewParamsForm, name='View Params')
        self.addForm('DetailViewParamsForm', DetailViewParamsForm, name='DetailView Params')
        self.addForm('TemplateViewParamsForm', TemplateViewParamsForm, name='TemplateView Params')


class Command(BaseCommand):
    args = ''
    help = 'Closes the specified poll for voting'

    def handle(self, app_name, **kwargs):
        API.set_app_name(app_name)
        npyscreen.wrapper_basic(self._gui)
        self.stdout.write('Dziala')

    def _gui(self, *args):
        self.app = MyApplication().run()
