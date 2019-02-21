"""
Django settings for SixcycleWiki project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2kj%%^khue249%e_*$q$^n+0s$mso$q3+(jf@n&*8wl9ffv+^j'
AWS_ACCESS_KEY_ID = 'AKIAII3MV3YTNHV2RPPA'
AWS_SECRET_ACCESS_KEY = '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'
from boto.s3.connection import SubdomainCallingFormat
AWS_CALLING_FORMAT = SubdomainCallingFormat

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'sixcycle-wiki-env.7dwtp34aiu.us-east-1.elasticbeanstalk.com',
    'wiki-stg.sixcycle.com',
    '127.0.0.1'
    ]
SITE_ID = 1
# WIKI_ACCOUNT_HANDLING = False

# Application definition

INSTALLED_APPS = [
    'authtools',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'storages',
    'boto3',
    'wiki',
    'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.links.apps.LinksConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'SixcycleWiki.authentication',
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

AUTHENTICATION_BACKENDS = [
    'SixcycleWiki.authentication_backend.MyBackend'
]


STATIC_ROOT = 'static'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


ROOT_URLCONF = 'SixcycleWiki.urls'
AUTH_USER_MODEL = 'authentication.ProxyUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

WSGI_APPLICATION = 'SixcycleWiki.wsgi.application'
AWS_STORAGE_BUCKET_NAME = 'sixcycle-wiki-storage'
AWS_S3_REGION_NAME = 'us-east-1'
WIKI_USE_LOCAL_PATH = False
WIKI_STORAGE_BACKEND = 'storages.backends.s3boto3.S3Boto3Storage'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SixCycleDB',
        'USER': 'sa',
        'PASSWORD': 'p0o9i8u7',
        'HOST': 'wiki-test.cd8omj5dryba.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# Adding these settings for application to work in HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
