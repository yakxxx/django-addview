# django-addview - Add views to Django app automatically

## What it does?

You never remember Class-Based-Views parameters?
Are you tired of reiterating over same mundane steps while adding new view?
Try django-addview.

## How it works?

Django-addview provides you a simple ncurses based gui to add new class-based or functional view.

* Creates class declaration (fill needed parameters, select model from dropdown etc.)
* Remembers all class-based attributes for you
* Creates template (empty, or copied from existing one)
* Adds entry to __urls.py__
* Cares about all imports

## Installation

`pip install django_addview`

## Usage

`./manage.py addview app_name`
