#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.build_py import build_py as _build_py
from django.core.management import call_command
import sys
import os

from registration import get_version


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


class build_py(_build_py):
    """
        build_py class extended to compile the locales
        from the .po source files in .mo files.
    """
    def run(self):
        try:
            # Use the management command to compile messages
            # django 1.9 does not need the chdir anymore
            os.chdir('registration')
            call_command("compilemessages")
            os.chdir('..')
        except ImportError:
            pass
        _build_py.run(self)

setup(
    name='django-registration-redux',
    version=get_version().replace(' ', '-'),
    description='An extensible user-registration application for Django',
    long_description=open('README.rst').read(),
    author='Andrew Cutler',
    author_email='macropin@gmail.com',
    url='https://github.com/macropin/django-registration',
    package_dir={'registration': 'registration'},
    packages=find_packages(exclude='test_app'),
    tests_require=['pytest-django'],
    cmdclass={'test': PyTest, 'build_py': build_py},
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)
