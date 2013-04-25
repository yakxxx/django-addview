import npyscreen
from .._api import API
from .._config_loader import logger


class ViewTypeForm(npyscreen.Form):
    next_view = {
        'View': 'ViewParamsForm',
        'DetailView': 'DetailViewParamsForm',
        'CreateView': 'CreateViewParamsForm',
        'DeleteView': 'DeleteViewParamsForm',
        'FormView': 'FormViewParamsForm',
        'UpdateView': 'UpdateViewParamsForm',
        'TemplateView': 'TemplateViewParamsForm',
        'ListView': 'ListViewParamsForm',
        'function_view': 'FunctionViewParamsForm'
    }
    choices = ['View', 'TemplateView', 'DetailView',
                'ListView', 'CreateView', 'DeleteView',
                'FormView', 'UpdateView', 'function_view'
              ]

    def create(self):
        self.view_type = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=14,
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
        logger.debug(self.parentApp.NEXT_ACTIVE_FORM)
