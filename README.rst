Add views to Django app automatically
=====================================

What it does?
-------------

Can't remember Class-Based-Views parameters? Are you tired of
reiterating the same mundane steps while adding a new view? Try
django-addview.

How it works?
-------------

Django-addview provides you with a simple ncurses based gui to add new
class-based or functional view.

-  Creates class declaration (fill needed parameters, select a model
   from the dropdown etc.)
-  Remembers all class-based attributes for you
-  Creates template (empty, or copied from existing one)
-  Adds entry to **urls.py**
-  Cares about all imports

Installation
------------

``pip install django_addview``

Usage
-----

``./manage.py addview app_name``

Screenshots
-----------

|screenshot 1| |screenshot 2| |screenshot 3| |screenshot 4|

.. |screenshot 1| image:: https://raw.github.com/yakxxx/django-addview/master/_screenshots/addview1.png?raw=true
.. |screenshot 2| image:: https://raw.github.com/yakxxx/django-addview/master/_screenshots/addview2.png?raw=true
.. |screenshot 3| image:: https://raw.github.com/yakxxx/django-addview/master/_screenshots/addview3.png?raw=true
.. |screenshot 4| image:: https://raw.github.com/yakxxx/django-addview/master/_screenshots/addview4.png?raw=true
