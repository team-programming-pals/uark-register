"""
Django settings for programmingpals project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import django_heroku
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/



#The secret key is stored in an environment variable on Heroku.
SECRET_KEY = os.getenv("SECRET_KEY", "!!SECRET_KEY_ENVIRONMENT_VARIBLE_NOT_SET!!")


"""
SECURITY WARNING: don't run with debug turned on in production!
This option will be left enabled to make development easier and
will be switched off once the project is complete.
"""
DEBUG = True

# All hosts are allowed during development to lessen potential configuration woes between team members.
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'register.apps.RegisterConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'programmingpals.urls'

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
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'programmingpals.wsgi.application'


"""
Database
https://docs.djangoproject.com/en/3.1/ref/settings/#databases

By default Heroku will store database information as an environment variable.
The dj_database_url module will automatically pull this information from your
Heroku instance and use it as the default database entry.
"""
#DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

DATABASES = {'default': dj_database_url.config(default='postgres://qmozdzzwkzbppv:50ff5a0c6ce1ad1f6f77d1c1baa529538cce567e9062c09422a3dd6af9969319@ec2-54-166-107-5.compute-1.amazonaws.com:5432/dc6eu7nlt659pq')}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Heroku recommends using whitenoise for static file storage
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Heroku settings
django_heroku.settings(locals())
