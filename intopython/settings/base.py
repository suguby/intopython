# -*- coding: utf-8 -*-

"""
Django settings for intopython project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '...'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'taggit',
    # 'django_pygments',
    'markdownx',
    'social_django',

    'src.articles',
    'src.blog',
    'src.screencasts',
    'src.courses',
    'src.landing',
    'src.registration',
    'src.payments'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'intopython.urls'

TEMPLATES = [
    {
        # http://niwinz.github.io/django-jinja/#_introduction_3
        "BACKEND": "django_jinja.backend.Jinja2",
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".html",
            "match_regex": r"^(?!(admin|debug_toolbar)/).*",
            # "match_regex": r"^(?!admin/).*",
            "app_dirname": "templates",
            # "autoescape": True,
            # "auto_reload": DEBUG,
            "filters": {
                "set_css_class": "src.common.css_filters.set_css_class",
            },
            'context_processors': (
                'src.common.context_processors.common_variables_to_context',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            )

        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        "APP_DIRS": True,
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

WSGI_APPLICATION = 'intopython.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '...',
        'USER': '...',
        'PASSWORD': '...',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'extra', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'extra', 'media')

FAB_SERVERS = {}
MYSQL_DUMPS_PATH = os.path.join(BASE_DIR, 'extra')
FAB_NOTIFY_TASK_ENDS = True

TAGGIT_CASE_INSENSITIVE = True

AUTH_USER_MODEL = 'registration.MyUser'
LOGIN_REDIRECT_URL = '/'

COURSES_REGISTRATION_EMAIL = 'intopython@intopython.ru'

MARKDOWNX_EDITOR_RESIZABLE = True

FORM_RENDERER = 'django.forms.renderers.Jinja2'
CSRF_USE_SESSIONS = True
