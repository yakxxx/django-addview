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
    BEGIN_ENTRY = 23

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
    BEGIN_ENTRY = 23

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


class TemplateMixin(object):
    BEGIN_ENTRY = 23

    def create(self):
        self.content_type = self.add(
            npyscreen.TitleText,
            name='content_type',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.template_name = self.add(
            npyscreen.TitleText,
            name='template_name',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.response_class = self.add(
            npyscreen.TitleText,
            name='response_class',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        self._view_params.update(
            {'content_type': self.content_type.value,
             'template_name': self.template_name.value,
             'response_class': self.response_class.value}
        )


class MultipleObjectTemplateMixin(TemplateMixin):
    BEGIN_ENTRY = 23

    def create(self):
        super(MultipleObjectTemplateMixin, self).create()
        self.template_name_suffix = self.add(
            npyscreen.TitleText,
            name='template_name_suffix',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        super(MultipleObjectTemplateMixin, self)._save_parameters()
        self._view_params.update(
            {'template_name_suffix': self.template_name_suffix.value}
        )


class SingleObjectTemplateMixin(MultipleObjectTemplateMixin):
    BEGIN_ENTRY = 23

    def create(self):
        super(SingleObjectTemplateMixin, self).create()
        self.template_name_field = self.add(
            npyscreen.TitleText,
            name='template_name_field',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        super(SingleObjectTemplateMixin, self)._save_parameters()
        self._view_params.update(
            {'template_name_field': self.template_name_field.value}
        )


class FormMixin(object):
    BEGIN_ENTRY = 23

    def create(self):
        self.form_class = self.add(
            npyscreen.TitleText,
            name='form_class',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.initial = self.add(
            npyscreen.TitleText,
            name='initial',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.success_url = self.add(
            npyscreen.TitleText,
            name='success_url',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        self._view_params.update(
            {'form_class': self.form_class.value,
             'initial': self.initial.value,
             'success_url': self.success_url.value}
        )


class ViewParamsForm(ViewForm):
    def create(self):
        super(ViewParamsForm, self).create()


class DetailViewParamsForm(ViewForm, SingleObjectMixin,
            SingleObjectTemplateMixin):
    def create(self):
        super(DetailViewParamsForm, self).create()
        SingleObjectMixin.create(self)
        SingleObjectTemplateMixin.create(self)

    def _save_parameters(self):
        super(DetailViewParamsForm, self)._save_parameters()
        SingleObjectTemplateMixin._save_parameters(self)
        SingleObjectMixin._save_parameters(self)


class CreateViewParamsForm(ViewForm, SingleObjectMixin,
             SingleObjectTemplateMixin, FormMixin):

    def create(self):
        super(CreateViewParamsForm, self).create()
        SingleObjectMixin.create(self)
        SingleObjectTemplateMixin.create(self)
        FormMixin.create(self)

    def _save_parameters(self):
        super(CreateViewParamsForm, self)._save_parameters()
        SingleObjectTemplateMixin._save_parameters(self)
        SingleObjectMixin._save_parameters(self)
        FormMixin._save_parameters(self)


class DeleteViewParamsForm(ViewForm, SingleObjectMixin,
             SingleObjectTemplateMixin):

    def create(self):
        super(DeleteViewParamsForm, self).create()
        SingleObjectMixin.create(self)
        SingleObjectTemplateMixin.create(self)
        self.success_url = self.add(
            npyscreen.TitleText,
            name='success_url',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        super(DeleteViewParamsForm, self)._save_parameters()
        SingleObjectTemplateMixin._save_parameters(self)
        SingleObjectMixin._save_parameters(self)
        self._view_params.update(
            {'success_url': self.success_url.value}
        )


class FormViewParamsForm(ViewForm, TemplateMixin, FormMixin):
    def create(self):
        super(FormViewParamsForm, self).create()
        TemplateMixin.create(self)
        FormMixin.create(self)

    def _save_parameters(self):
        super(FormViewParamsForm, self)._save_parameters()
        TemplateMixin._save_parameters(self)
        FormMixin._save_parameters(self)


class UpdateViewParamsForm(ViewForm, SingleObjectMixin,
        SingleObjectTemplateMixin, FormMixin):

    def create(self):
        super(UpdateViewParamsForm, self).create()
        SingleObjectMixin.create(self)
        SingleObjectTemplateMixin.create(self)
        FormMixin.create(self)

    def _save_parameters(self):
        super(UpdateViewParamsForm, self)._save_parameters()
        SingleObjectMixin._save_parameters(self)
        SingleObjectTemplateMixin._save_parameters(self)
        FormMixin.create(self)


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
