from django.core.management.base import BaseCommand
import npyscreen

from ._api import Api, API
from ._config_loader import logger, tmp_logs

from .forms.view_type import ViewTypeForm
from .forms.view_params import DetailViewParamsForm, FunctionViewParamsForm, \
    ListViewParamsForm, TemplateViewParamsForm, ViewParamsForm, \
    CreateViewParamsForm, DeleteViewParamsForm, FormViewParamsForm, \
    UpdateViewParamsForm
from .forms.template_params import TemplateForm
from .forms.urls_conf import UrlsForm


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', ViewTypeForm, name='View Type')
        self.addForm(
            'ViewParamsForm',
            ViewParamsForm,
            name='View Params'
        )
        self.addForm(
            'DetailViewParamsForm',
            DetailViewParamsForm,
            name='DetailView Params'
        )
        self.addForm(
            'CreateViewParamsForm',
             CreateViewParamsForm,
             name="Create form"
        )
        self.addForm(
            'DeleteViewParamsForm',
             DeleteViewParamsForm,
             name="Delete form"
        )
        self.addForm(
            'FormViewParamsForm',
             FormViewParamsForm,
             name="Form form"
        )
        self.addForm(
            'UpdateViewParamsForm',
             UpdateViewParamsForm,
             name="Create form"
        )
        self.addForm(
            'TemplateViewParamsForm',
            TemplateViewParamsForm,
            name='TemplateView Params'
        )
        self.addForm(
            'ListViewParamsForm',
            ListViewParamsForm,
            name='ListView Params'
        )
        self.addForm(
            'UrlsForm',
            UrlsForm,
            name='Urls form'
        )
        self.addForm(
            'TemplateForm',
             TemplateForm,
             name="Template form"
        )


class Command(BaseCommand):
    args = ''
    help = 'Closes the specified poll for voting'

    def handle(self, app_name, **kwargs):
        import atexit
        atexit.register(self._show_logs)
        API.set_app_name(app_name)
        npyscreen.wrapper_basic(self._gui)
        logger.info('Finished!')

    def _gui(self, *args):
        self.app = MyApplication().run()

    def _show_logs(self):
        self.stdout.write('=============LOGS=================')
        self.stdout.write(tmp_logs.getvalue())
