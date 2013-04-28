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

## Screenshots
![screenshot 1](/_screenshots/addview1.png?raw=true)
![screenshot 2](/_screenshots/addview2.png?raw=true)
![screenshot 3](/_screenshots/addview3.png?raw=true)
![screenshot 4](/_screenshots/addview4.png?raw=true)
