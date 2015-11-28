from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

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
    cmdclass={'test': PyTest},
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
