.. -*-restructuredtext-*-

:Description: Django-registration provides user registration functionality for Django websites.
:maintainers: Macropin_, DiCato_, and joshblum_
:contributors: `list of contributors <https://github.com/macropin/django-registration/graphs/contributors>`_

.. _Macropin: https://github.com/macropin
.. _DiCato: https://github.com/dicato
.. _joshblum: https://github.com/joshblum

.. image:: https://github.com/macropin/django-registration/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/macropin/django-registration/actions

.. image:: https://coveralls.io/repos/macropin/django-registration/badge.svg?branch=main
    :target: https://coveralls.io/r/macropin/django-registration/

.. image:: https://badge.fury.io/py/django-registration-redux.svg
    :target: https://pypi.python.org/pypi/django-registration-redux/

.. image:: https://readthedocs.org/projects/django-registration-redux/badge/?version=latest
    :target: http://django-registration-redux.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/django-registration-redux.svg
    :target: https://pypi.python.org/pypi/django-registration-redux
.. image:: https://img.shields.io/badge/_4.2_|_5.0-blue?color=0C4B33&label=django&logo=django&logoColor=white
    :target: https://github.com/django/django

If you have issues with the "django-registration-redux" package then please `raise them here`_.

This is a fairly simple user-registration application for Django, designed to
make allowing user signups as painless as possible. It requires a functional
installation of Django 3.1 or newer, but has no other dependencies.


Installation
------------

Install, upgrade and uninstall django-registration-redux with these commands::

    pip install django-registration-redux
    pip install --upgrade django-registration-redux
    pip uninstall django-registration-redux

To install it manually, run the following command inside this source directory::

    python setup.py install


Or if you'd prefer you can simply place the included ``registration``
directory somewhere on your Python path, or symlink to it from
somewhere on your Python path; this is useful if you're working from a
Git checkout.

Note that this application requires Python 3.5 or later, and a
functional installation of Django 3.1 or newer.

If you are running on Django <=2.0, you can install a previous version of
`django-registration-redux`, which supports older versions of Django. See the
`CHANGELOG`_ for support details. Older versions will receive minor bug fixes as
needed, but are no longer actively developed::

    pip install django-registration-redux==1.10


Getting started with development
--------------------------------

To get started with development, first install the required packages::

    make installdeps

For convenience a ``Makefile`` is included which wraps the Python `invoke
<http://www.pyinvoke.org/>`_ library. Once you work on a patch, you can test
the functionality by running::

    make test

Or equivalently::

    invoke test

Command line arguments can be passed to the ``invoke`` script through the
``Makefile`` via the ``ARGS`` parameter. For example::

    make build ARGS=--docs

Or equivalently::

    invoke build --docs

Alternatives
------------

`djangopackages.com <https://www.djangopackages.com/grids/g/registration/>`_
has a comprehensive comparison of Django packages used for user registration
and authentication.

For example, `django-allauth <http://www.intenct.nl/projects/django-allauth/>`_
is an alternative to django-registration-redux that provides user registration
in addition to social authentication and email address management.

License
-------

Django-registration-redux is licensed under `BSD License`.



.. _`available online`: https://django-registration-redux.readthedocs.org/
.. _`raise them here`: https://github.com/macropin/django-registration/issues
.. _`CHANGELOG`: https://github.com/macropin/django-registration/blob/main/CHANGELOG
