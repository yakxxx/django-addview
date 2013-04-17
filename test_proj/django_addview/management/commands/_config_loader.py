import os
import django
PROJ_ROOT = os.path.dirname(os.path.realpath(django.__file__))

config = {
    'template_dir': os.path.join('{app_path}', 'templates')
}
