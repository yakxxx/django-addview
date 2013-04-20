from django.core.management.base import BaseCommand
import npyscreen
import logging

from _api import Api
from _config_loader import logger
API = Api()


class TemplateForm(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        self._view_params = {}
        self._tpl_creation_choices = \
            ['Create empty', 'Don\'t create'] + \
            ['copy {0}'.format(file_name)
              for file_name in sorted(API.get_template_filenames())]
        super(TemplateForm, self).__init__(*args, **kwargs)

    def create(self):
        self._template_name = self.add(npyscreen.TitleText, name='template_name')

        self._template_creation = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=7,
            name='Create template from:',
            values=self._tpl_creation_choices,
            value=0
        )

    def afterEditing(self):
        self._save_parameters()
        API.create_view(self._view_params)

    def _save_parameters(self):
        template_names = sorted(API.get_template_filenames())
        template_create_from = \
            '' if self._template_creation.value[0] == 0 else \
            None if self._template_creation.value[0] == 1 else \
            template_names[self._template_creation.value[0] - 2]

        self._view_params.update(
            {'template_name': self._template_name.value,
             'template_create_from': template_create_from}
        )


class SingleObjectMixin(object):
    BEGIN_ENTRY = 22

    def create(self):
        self.model = self.add(
            npyscreen.TitleText,
            name='model',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.queryset = self.add(
            npyscreen.TitleText,
            name='queryset',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.slug_field = self.add(
            npyscreen.TitleText,
            name='slug_field',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.slug_url_kwarg = self.add(
            npyscreen.TitleText,
            name='slug_url_kwarg',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.pk_url_kwarg = self.add(
            npyscreen.TitleText,
            name='pk_url_kwarg',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.context_object_name = self.add(
            npyscreen.TitleText,
            name='context_object_name',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        self._view_params.update(
            {'model': self.model.value,
             'queryset': self.queryset.value,
             'slug_field': self.slug_field.value,
             'slug_url_kwarg': self.slug_url_kwarg.value,
             'pk_url_kwarg': self.pk_url_kwarg.value,
             'context_object_name': self.context_object_name.value}
        )


class MultipleObjectMixin(object):
    BEGIN_ENTRY = 22

    def create(self):
        self.allow_empty = self.add(
            npyscreen.TitleSelectOne,
            name='allow_empty',
            values=['True', 'False'],
            value=0,
            max_height=2,
            scroll_exit=True,
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.model = self.add(
            npyscreen.TitleText,
            name='model',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.queryset = self.add(
            npyscreen.TitleText,
            name='queryset',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.paginate_by = self.add(
            npyscreen.TitleText,
            name='paginate_by',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.page_kwarg = self.add(
            npyscreen.TitleText,
            name='page_kwarg',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.paginator_class = self.add(
            npyscreen.TitleText,
            name='paginator_class',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.context_object_name = self.add(
            npyscreen.TitleText,
            name='context_object_name',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        self._view_params.update(
            {'model': self.model.value,
             'allow_empty': self.allow_empty.value,
             'queryset': self.queryset.value,
             'paginate_by': self.paginate_by.value,
             'page_kwarg': self.page_kwarg.value,
             'paginator_class': self.paginator_class.value,
             'context_object_name': self.context_object_name.value}
        )


class ViewParamsForm(TemplateForm):
    def create(self):
        self.myName = self.add(npyscreen.TitleText, name='Name')
        super(ViewParamsForm, self).create()


class DetailViewParamsForm(TemplateForm, SingleObjectMixin):
    def create(self):
        super(DetailViewParamsForm, self).create()
        SingleObjectMixin.create(self)

    def _save_parameters(self):
        super(DetailViewParamsForm, self)._save_parameters()
        SingleObjectMixin._save_parameters(self)


class TemplateViewParamsForm(TemplateForm):
    def create(self):
        super(TemplateViewParamsForm, self).create()

#    def _save_parameters(self):
#        super(TemplateViewParamsForm, self)._save_parameters()
#        self._view_params.update(
#            {'model': self.model.value}
#        )


class ListViewParamsForm(TemplateForm, MultipleObjectMixin):
    def create(self):
        super(ListViewParamsForm, self).create()
        MultipleObjectMixin.create(self)

    def _save_parameters(self):
        super(ListViewParamsForm, self)._save_parameters()
        MultipleObjectMixin._save_parameters(self)

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
            value=0,
            name='View Type',
            values=self.choices
        )

    def afterEditing(self):
        try:
            view_type_value = self.view_type.value[0]
        except IndexError:
            view_type_value = None

        choice = self.choices[view_type_value]

        self.parentApp.NEXT_ACTIVE_FORM = self.next_view.get(
            choice,
            None
        )
        API.set_view_type(choice)
        logger.warn(self.parentApp.NEXT_ACTIVE_FORM)


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
            'TemplateViewParamsForm',
            TemplateViewParamsForm,
            name='TemplateView Params'
        )
        self.addForm(
            'ListViewParamsForm',
            ListViewParamsForm,
            name='ListView Params'
        )


class Command(BaseCommand):
    args = ''
    help = 'Closes the specified poll for voting'

    def handle(self, app_name, **kwargs):
        API.set_app_name(app_name)
        npyscreen.wrapper_basic(self._gui)
        self.stdout.write('Dziala')

    def _gui(self, *args):
        self.app = MyApplication().run()
