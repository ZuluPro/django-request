pony-traffic
============

.. image:: https://api.travis-ci.org/ZuluPro/pony-traffic.svg
        :target: https://travis-ci.org/ZuluPro/pony-traffic

Pony Traffic is a for of `django-request`_ and a statistics module for django. It stores requests in a database for admins to see, it can also be used to get statistics on who is online etc. This fork aims to store visitor and visit and go deeper in "What users do ?"

.. image:: docs/graph.png

As well as a site statistics module, with the active_users template tag and manager method you can also use django-request to show who is online in a certain time. ::

    Request.objects.active_users(minutes=15)

To find the request overview page, please click on Requests inside the admin, then “Overview” on the top right, next to “add”.

Installation
------------

- Put `'request'`  and `'request.tracking'` in your INSTALLED_APPS setting.
- Run the command `manage.py syncdb`.
- Add `request.middleware.RequestMiddleware` to `MIDDLEWARE_CLASSES`. If you use `django.contrib.auth`, place the RequestMiddleware after it. If you use `django.contrib.flatpages` place `request.middleware.RequestMiddleware` before it else flatpages will be marked as error pages in the admin panel.
- Make sure that the domain name in `django.contrib.sites` admin is correct. This is used to calculate unique visitors and top referrers.


Detailed documentation
----------------------

This project is under heavy development, as it is a fork, the documentation may be out-dated. You can consult `django-request documentation`_ which is core of this project.


.. _`django-request`: https://github.com/django-request/django-request
.. _`django-request documentation`: https://django-request.readthedocs.org/en/latest/
