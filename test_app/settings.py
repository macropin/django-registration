# coding: utf-8


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'registration',
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'registration',
    'test_app',
)

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'aa2^x-^2u9(zaigih^7!3onca_rql1rnk6ec6=sahm*r$vd2-$)=5'

SITE_ID = 1

ROOT_URLCONF = 'test_app.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = ""