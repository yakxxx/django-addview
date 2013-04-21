import npyscreen
from .._api import API


class ViewForm(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        self._view_params = {}
        self._tpl_creation_choices = \
            ['Create empty', 'Don\'t create'] + \
            ['copy {0}'.format(file_name)
              for file_name in API.get_template_filenames()]
        super(ViewForm, self).__init__(*args, **kwargs)

    def create(self):
        self.class_name = self.add(
            npyscreen.TitleText,
            name='ClassName'
        )

        self.template_name = self.add(
            npyscreen.TitleText,
            name='template_name'
        )

    def afterEditing(self):
        self._save_parameters()
        API.update_view_params(self._view_params)
        if self._view_params.get('class_name', None):
            self.parentApp.NEXT_ACTIVE_FORM = 'TemplateForm'
        else:
            npyscreen.notify_wait(
                "You have to set ClassName",
                 "Form Validation"
            )

    def _save_parameters(self):
        self._view_params.update(
            {'class_name': self.class_name.value,
             'template_name': self.template_name.value, }
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


class ViewParamsForm(ViewForm):
    def create(self):
        super(ViewParamsForm, self).create()


class DetailViewParamsForm(ViewForm, SingleObjectMixin):
    def create(self):
        super(DetailViewParamsForm, self).create()
        SingleObjectMixin.create(self)

    def _save_parameters(self):
        super(DetailViewParamsForm, self)._save_parameters()
        SingleObjectMixin._save_parameters(self)


class TemplateViewParamsForm(ViewForm):
    def create(self):
        super(TemplateViewParamsForm, self).create()

#    def _save_parameters(self):
#        super(TemplateViewParamsForm, self)._save_parameters()
#        self._view_params.update(
#            {'model': self.model.value}
#        )


class ListViewParamsForm(ViewForm, MultipleObjectMixin):
    def create(self):
        super(ListViewParamsForm, self).create()
        MultipleObjectMixin.create(self)

    def _save_parameters(self):
        super(ListViewParamsForm, self)._save_parameters()
        MultipleObjectMixin._save_parameters(self)


class FunctionViewParamsForm(npyscreen.Form):
    def create(self):
        self.myName = self.add(npyscreen.TitleText, name='Name')
