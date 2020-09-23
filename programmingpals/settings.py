"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/topics/settings/
    2. https://docs.djangoproject.com/en/3.1/ref/databases/
    3. https://docs.djangoproject.com/en/3.1/intro/tutorial01/
    4. https://devcenter.heroku.com/articles/getting-started-with-python
    5. https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
"""

import django_heroku
import dj_database_url
from pathlib import Path
from os import getenv, path


# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


"""
The SECRET_KEY for our register is stored inside of an environment variable
named "SECRET_KEY" on Heroku. When the web application is ran locally, it will
default to using "!!SECRET_KEY_ENVIRONMENT_VARIBLE_NOT_SET!!" as a temporary
secret key.
"""
SECRET_KEY = getenv("SECRET_KEY", "!!SECRET_KEY_ENVIRONMENT_VARIBLE_NOT_SET!!")


# Set DEBUG to False before pushing to GitHub. Set it to true for local testing though
DEBUG = True


# Django can serve these hosts. This will prevent HTTP host header attacks
ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]', '.herokuapp.com']


# Applications registered with Django
INSTALLED_APPS = [
    'register.apps.RegisterConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]


# Django plugins that extend what the framrwork can do
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


# Tell Django where our URLS file is located
ROOT_URLCONF = 'programmingpals.urls'


# This is the system Django uses to processs our templates
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


# Expose our web application to any WSGI-compliant web server
WSGI_APPLICATION = 'programmingpals.wsgi.application'

""" 
This will tell Django how to connect to our Heroku hosted database. Make
sure this is the only database entry in this settings file before you push
your code to GitHub

Failure to follow this rule will cause our live demo to eventually break and
will expose our database username/password to anyone who looks at the code
"""
#DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}


# You can comment out the database entry above and add a new entry below this line for local testing
DATABASES = {'default': dj_database_url.config(default='postgres://qmozdzzwkzbppv:50ff5a0c6ce1ad1f6f77d1c1baa529538cce567e9062c09422a3dd6af9969319@ec2-54-166-107-5.compute-1.amazonaws.com:5432/dc6eu7nlt659pq')}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'


# Compress our static content
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    path.join(BASE_DIR, 'static'),
)


# Heroku settings
django_heroku.settings(locals())

#Test comment for commit