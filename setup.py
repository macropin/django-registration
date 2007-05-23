from distutils.core import setup

setup(name='registration',
      version='0.1',
      description='User-registration application for Django',
      author='James Bennett',
      author_email='james@b-list.org',
      url='http://code.google.com/p/django-registration/',
      packages=['registration'],
      package_dir={ 'registration': 'registration' },
      package_data={ 'registration': ['templates/registration/*.*'] },
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
