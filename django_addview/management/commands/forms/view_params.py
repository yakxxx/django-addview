import npyscreen
from .._api import API


class ViewForm(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        self._view_params = {}
        self._widgets = []
        self._tpl_creation_choices = \
            ['Create empty', 'Don\'t create'] + \
            ['copy {0}'.format(file_name)
              for file_name in API.get_template_filenames()]
        super(ViewForm, self).__init__(*args, **kwargs)

    def create(self):
        self.add_later(
            npyscreen.TitleText,
            attr_name='class_name',
            name='ClassName',
            show_order=1000
        )
        self._create()
        for priority, _args, _kwargs in sorted(self._widgets):
            attr_name = _kwargs.pop('attr_name')
            setattr(self, attr_name, self.add(*_args, **_kwargs))

    def _create(self):
        pass

    def add_later(self, *args, **kwargs):
        priority = kwargs.pop('show_order', 0)
        self._widgets.append((-priority, args, kwargs))

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
            {'class_name': self.class_name.value}
        )


class SingleObjectMixin(object):
    BEGIN_ENTRY = 23

    def _create(self):
        self.add_later(
            npyscreen.TitleSelectOne,
            attr_name='model',
            values=['Leave empty'] + API.get_model_names(),
            value=0,
            max_height=5,
            name='model',
            scroll_exit=True,
            show_order=100,
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='queryset',
            name='queryset',
            show_order=20,
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='slug_field',
            name='slug_field',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='slug_url_kwarg',
            name='slug_url_kwarg',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='pk_url_kwarg',
            name='pk_url_kwarg',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='context_object_name',
            name='context_object_name',
            show_order=10,
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        self._view_params.update(
            {'model': ([''] + API.get_model_names())[self.model.value[0]],
             'queryset': self.queryset.value,
             'slug_field': self.slug_field.value,
             'slug_url_kwarg': self.slug_url_kwarg.value,
             'pk_url_kwarg': self.pk_url_kwarg.value,
             'context_object_name': self.context_object_name.value}
        )


class MultipleObjectMixin(object):
    BEGIN_ENTRY = 23

    def _create(self):
        self.add_later(
            npyscreen.TitleSelectOne,
            attr_name='allow_empty',
            name='allow_empty',
            values=['True', 'False'],
            value=0,
            max_height=2,
            scroll_exit=True,
            show_order=1,
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleSelectOne,
            attr_name='model',
            values=['Leave empty'] + API.get_model_names(),
            value=0,
            max_height=5,
            name='model',
            scroll_exit=True,
            show_order=100,
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='queryset',
            name='queryset',
            show_order=20,
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='paginate_by',
            name='paginate_by',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='page_kwarg',
            name='page_kwarg',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='paginator_class',
            name='paginator_class',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='context_object_name',
            name='context_object_name',
            begin_entry_at=self.BEGIN_ENTRY
        )

    def _save_parameters(self):
        self._view_params.update(
            {'model': ([''] + API.get_model_names())[self.model.value[0]],
             'allow_empty': ['True', 'False'][self.allow_empty.value[0]],
             'queryset': self.queryset.value,
             'paginate_by': self.paginate_by.value,
             'page_kwarg': self.page_kwarg.value,
             'paginator_class': self.paginator_class.value,
             'context_object_name': self.context_object_name.value}
        )


class TemplateMixin(object):
    BEGIN_ENTRY = 23

    def _create(self):
        self.add_later(
            npyscreen.TitleText,
            attr_name='content_type',
            name='content_type',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='template_name',
            name='template_name',
            begin_entry_at=self.BEGIN_ENTRY,
            show_order=50
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='response_class',
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

    def _create(self):
        super(MultipleObjectTemplateMixin, self)._create()
        self.add_later(
            npyscreen.TitleText,
            attr_name='template_name_suffix',
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

    def _create(self):
        super(SingleObjectTemplateMixin, self)._create()
        self.add_later(
            npyscreen.TitleText,
            attr_name='template_name_field',
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

    def _create(self):
        self.add_later(
            npyscreen.TitleText,
            attr_name='form_class',
            show_order=24,
            name='form_class',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            show_order=23,
            attr_name='initial',
            name='initial',
            begin_entry_at=self.BEGIN_ENTRY
        )
        self.add_later(
            npyscreen.TitleText,
            attr_name='success_url',
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
    def _create(self):
        super(ViewParamsForm, self)._create()


class DetailViewParamsForm(ViewForm, SingleObjectMixin,
            SingleObjectTemplateMixin):
    def _create(self):
        super(DetailViewParamsForm, self)._create()
        SingleObjectMixin._create(self)
        SingleObjectTemplateMixin._create(self)

    def _save_parameters(self):
        super(DetailViewParamsForm, self)._save_parameters()
        SingleObjectTemplateMixin._save_parameters(self)
        SingleObjectMixin._save_parameters(self)


class CreateViewParamsForm(ViewForm, SingleObjectMixin,
             SingleObjectTemplateMixin, FormMixin):

    def _create(self):
        super(CreateViewParamsForm, self)._create()
        SingleObjectMixin._create(self)
        SingleObjectTemplateMixin._create(self)
        FormMixin._create(self)

    def _save_parameters(self):
        super(CreateViewParamsForm, self)._save_parameters()
        SingleObjectTemplateMixin._save_parameters(self)
        SingleObjectMixin._save_parameters(self)
        FormMixin._save_parameters(self)


class DeleteViewParamsForm(ViewForm, SingleObjectMixin,
             SingleObjectTemplateMixin):

    def _create(self):
        super(DeleteViewParamsForm, self)._create()
        SingleObjectMixin._create(self)
        SingleObjectTemplateMixin._create(self)
        self.add_later(
            npyscreen.TitleText,
            attr_name='success_url',
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
    def _create(self):
        super(FormViewParamsForm, self)._create()
        TemplateMixin._create(self)
        FormMixin._create(self)

    def _save_parameters(self):
        super(FormViewParamsForm, self)._save_parameters()
        TemplateMixin._save_parameters(self)
        FormMixin._save_parameters(self)


class UpdateViewParamsForm(ViewForm, SingleObjectMixin,
        SingleObjectTemplateMixin, FormMixin):

    def _create(self):
        super(UpdateViewParamsForm, self)._create()
        SingleObjectMixin._create(self)
        SingleObjectTemplateMixin._create(self)
        FormMixin._create(self)

    def _save_parameters(self):
        super(UpdateViewParamsForm, self)._save_parameters()
        SingleObjectMixin._save_parameters(self)
        SingleObjectTemplateMixin._save_parameters(self)
        FormMixin._create(self)


class TemplateViewParamsForm(ViewForm, TemplateMixin):
    def _create(self):
        super(TemplateViewParamsForm, self)._create()
        TemplateMixin._create(self)

    def _save_parameters(self):
        super(TemplateViewParamsForm, self)._save_parameters()
        TemplateMixin._save_parameters(self)


class ListViewParamsForm(ViewForm, MultipleObjectMixin,
            MultipleObjectTemplateMixin):
    def _create(self):
        super(ListViewParamsForm, self)._create()
        MultipleObjectMixin._create(self)
        MultipleObjectTemplateMixin._create(self)

    def _save_parameters(self):
        super(ListViewParamsForm, self)._save_parameters()
        MultipleObjectMixin._save_parameters(self)
        MultipleObjectTemplateMixin._save_parameters(self)


class FunctionViewParamsForm(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        super(FunctionViewParamsForm, self).__init__(*args, **kwargs)
        self._view_params = {}

    def create(self):
        self.function_name = self.add(
            npyscreen.TitleText,
            attr_name='function_name',
            name='function name'
        )

    def afterEditing(self):
        self._save_parameters()
        API.update_view_params(self._view_params)
        if self._view_params.get('function_name', None):
            self.parentApp.NEXT_ACTIVE_FORM = 'TemplateForm'
        else:
            npyscreen.notify_wait(
                "You have to set function_name",
                 "Form Validation"
            )

    def _save_parameters(self):
        self._view_params.update(
            {'function_name': self.function_name.value}
        )
