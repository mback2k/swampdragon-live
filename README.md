[SwampDragon-live](https://github.com/mback2k/swampdragon-live) is an
extension to [Django](https://www.djangoproject.com/) and
[SwampDragon](http://swampdragon.net/) with SwampDragon-auth and Celery
which adds support for live updating Django template snippets on model changes.

Installation
------------
Install the latest version from pypi.python.org:

    pip install SwampDragon-live

Install the development version by cloning the source from github.com:

    pip install git+https://github.com/mback2k/swampdragon-live.git

At the moment Django 1.8 and Celery are required dependencies.

Configuration
-------------
Add the package to your `INSTALLED_APPS`:

    INSTALLED_APPS += (
        'swampdragon',
        'swampdragon_live',
    )

Example
-------
Make sure to add the following line to your Django settings file:

    SWAMP_DRAGON_CONNECTION = ('swampdragon_auth.socketconnection.HttpDataConnection', '/data')

Load the required JavaScript template-tags within your Django template:

    {% load swampdragon_tags %}
    {% load swampdragon_live %}

Add the required JavaScript to your Django template:

    {% swampdragon_settings %}
    <script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/dist/swampdragon.min.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/dist/swampdragon.live.js"></script>

Use the include_live template-tag instead of the default include template-tag,
with rows being a Django database QuerySet to listen for added, changed, deleted instances:

    {% include_live 'table' 'includes/table_body.html' rows=rows perms=perms %}

Use the include_live template-tag instead of the default include template-tag,
with row being a single Django database Model instance to listen for changes:

    {% include_live 'tr' 'includes/row_cols.html' row=row perms=perms %}

A real-world example can be found in the Django project WebGCal:
* https://github.com/mback2k/django-webgcal/blob/master/webgcal/apps/webgcal/templates/show_dashboard.html
* https://github.com/mback2k/django-webgcal/tree/master/webgcal/apps/webgcal/templates/includes

License
-------
* Released under MIT License
* Copyright (c) 2015-2016 Marc Hoersken <info@marc-hoersken.de>