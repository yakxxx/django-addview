import os
import django
import logging
logger = logging.getLogger('addview')
hdlr = logging.FileHandler('addview.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

PROJ_ROOT = os.path.dirname(os.path.realpath(django.__file__))

config = {
    'template_dir': os.path.join('{app_path}', 'templates')
}
