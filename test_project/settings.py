"""
Django settings for running tests for rolca-core package.

"""
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'secret'

DEBUG = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'rolca_core',
)

ROOT_URLCONF = 'test_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('ROLCA_POSTGRESQL_NAME', 'rolca'),
        'USER': os.environ.get('ROLCA_POSTGRESQL_USER', 'rolca'),
        'PASSWORD': os.environ.get('ROLCA_POSTGRESQL_PASSWORD', 'rolca'),
        'HOST': os.environ.get('ROLCA_POSTGRESQL_HOST', 'localhost'),
        'PORT': int(os.environ.get('ROLCA_POSTGRESQL_PORT', 5432)),
    }
}

STATIC_URL = '/static/'
