"""
Django settings for cub project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Per Environment settings
APP_ENVIRONMENT = os.environ.get('APP_ENVIRONMENT', 'DEV')

if APP_ENVIRONMENT == 'DEV':
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'bu0-nf-yu99^$7!8z$#uiz22v6y&3-#i35&f3!s7e+u3ocs*3m'
    ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '192.168.3.3']
    DEBUG = True
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'cub.sqlite3'
        }
    }

    MONGO_CONFIG = {
        'HOST': '127.0.0.1',
        'PORT': 27017,
        'NAME': 'cub',
        'USER': '',
        'PASSWORD': ''
    }

elif APP_ENVIRONMENT == 'PROD':
    SECRET_KEY = os.environ.get('SECRET_KEY')

    ALLOWED_HOSTS = ['connecthub.herokuapp.com']
    ALLOWED_INCLUDE_ROOTS = [os.path.join(BASE_DIR)]

    CSRF_COOKIE_SECURE = True
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    DEBUG = False

    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}

    MONGO_CONFIG = {
        'HOST': 'ds035975.mongolab.com',
        'PORT': 35975,
        'NAME': 'heroku_gjd3tpfs',
        'USER': 'heroku_gjd3tpfs',
        'PASSWORD': 'heroku_gjd3tpfs',
    }

WSGI_APPLICATION = 'cub.wsgi.application'
# General settings

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
    'tastypie',
    'tastypie_mongoengine',
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

AUTH_USER_MODEL = 'backend.Account'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

ROOT_URLCONF = 'cub.urls'

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

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)
STATIC_URL = '/static/'

TASTYPIE_DEFAULT_FORMATS = ['json']
