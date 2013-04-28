# Add views to Django app automatically

## What it does?

Can't remember Class-Based-Views parameters?
Are you tired of reiterating the same mundane steps while adding a new view?
Try django-addview.

## How it works?

Django-addview provides you with a simple ncurses based gui to add new class-based or functional view.

* Creates class declaration (fill needed parameters, select a model from the dropdown etc.)
* Remembers all class-based attributes for you
* Creates template (empty, or copied from existing one)
* Adds entry to __urls.py__
* Cares about all imports

## Installation

`pip install django_addview`

## Usage

`./manage.py addview app_name`

## Configuration
Django-addview expects only one config variable. It's : `ADDVIEW_GLOBAL_TEMPLATE_DIR = ...`
which points to directory where you keep your project templates 
(It's good practice to keep templates inside one directory per project unless you write reusable app).

Django-addview can create your views in two locations. One is `ADDVIEW_GLOBAL_TEMPLATE_DIR` and second is `templates`
directory inside your apps directory. You choose between them while adding view in gui.

Example of configuration:

```
SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
ADDVIEW_GLOBAL_TEMPLATE_DIR = os.path.join(SITE_ROOT, 'templates')

```

## Screenshots
![screenshot 1](/_screenshots/addview1.png?raw=true)
![screenshot 2](/_screenshots/addview2.png?raw=true)
![screenshot 3](/_screenshots/addview3.png?raw=true)
![screenshot 4](/_screenshots/addview4.png?raw=true)
