import npyscreen
from .._api import API


class UrlsForm(npyscreen.Form):
    def create(self):
        self.urls_to_edit = self.add(
            npyscreen.TitleSelectOne,
            scroll_exit=True,
            max_height=3,
            value=0,
            name='urls.conf to edit',
            values=['Project global', 'Local for app', 'Don\'t edit']
        )
        self.url_regexp = self.add(
            npyscreen.TitleText,
            name='url pattern regexp',
            begin_entry_at=22,
            value="r'^put_pattern_here/'"
        )
        self.url_name = self.add(
            npyscreen.TitleText,
            name='url pattern name',
            begin_entry_at=22
        )

    def afterEditing(self):
        API.update_view_params(
            {'url_name': self.url_name.value,
             'url_pattern': self.url_regexp.value,
             'urls_to_edit':
                ('global', 'local', None)[
                    self.urls_to_edit.value[0]
                ]
            }
        )
        API.add_view()
        self.parentApp.NEXT_ACTIVE_FORM = None
