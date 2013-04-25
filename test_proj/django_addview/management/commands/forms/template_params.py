import npyscreen

from .._api import API


class TemplateForm(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        self._view_params = {}
        self._tpl_creation_choices = \
            ['Create empty', 'Don\'t create'] + \
            ['copy {0}'.format(file_name)
              for file_name in API.get_template_filenames()]
        super(TemplateForm, self).__init__(*args, **kwargs)

    def beforeEditing(self):
        self.template_name.value = API.get_template_name()

    def create(self):
        self.template_name = self.add(
            npyscreen.TitleText,
            name='template name',
        )
        self.template_creation = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=7,
            name='Create template from:',
            values=self._tpl_creation_choices,
            value=0
        )

        self.template_dir_choice = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=2,
            name='Directory to save template:',
            values=['Global for project', 'Local for app'],
            value=0,
        )

    def afterEditing(self):
        self._save_parameters()
        API.update_view_params(self._view_params)
        self.parentApp.NEXT_ACTIVE_FORM = 'UrlsForm'

    def _save_parameters(self):
        template_names = API.get_template_filenames()
        template_create_from = \
            '' if self.template_creation.value[0] == 0 else \
            None if self.template_creation.value[0] == 1 else \
            template_names[self.template_creation.value[0] - 2]

        self._view_params.update(
            {'template_create_from': template_create_from,
             'template_dir_choice':
                ('global', 'local')[self.template_dir_choice.value[0]]
            }
        )
