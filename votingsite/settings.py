"""
Django settings for votingsite project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'votingsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['polls/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'votingsite.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Load secrets and environment specific settings based on which
# environment we are currently in
# Note: The following is ignored by coverage reports.
if 'CI' in os.environ:  # noqa
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = True
    ALLOWED_HOSTS = []

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

elif 'HEROKU' in os.environ:  # noqa
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False
    ALLOWED_HOSTS = [os.environ['ALLOWED_HOST']]

    # redirect all http to https
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config()
    }

    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

else:  # noqa
    from votingsite import local_config
    SECRET_KEY = local_config.APP_SECRET_KEY
    DEBUG = local_config.APP_DEBUG
    ALLOWED_HOSTS = local_config.APP_ALLOWED_HOSTS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
