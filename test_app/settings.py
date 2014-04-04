# -*- coding: utf-8 -*-
'''
Created on 15.08.2013

@author: Michael Vorotyntsev (https://github.com/unaxfromsibiria/)
'''

import os
import re
import tempfile

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Michael Vorotyntsev', 'linkofwise@gmail.com'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
try:
    DIR_VERSION = re.findall(r'.+/(?P<version>[_0-9]{8,16})_.+', PROJECT_ROOT)[0]
except:
    import time
    DIR_VERSION = time.time()

TIME_ZONE = 'GMT'
LANGUAGE_CODE = 'ru'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static', 'content', 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static', 'content'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(tempfile.gettempdir(), 'test_app_main.db'),
    }
}

DJANGO_REDISCACHE = {
    'scheme': {
        'app.models.Model1': {'all': 300},
        'app.models.Model2': {'all': 300},
        'app.models.Model3': {'all': 300},
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'socket_timeout': 5,
        'pool': {
            'size': 20,
            'class': 'django_rediscache.pool.GeventConnectionPool',
        },
    },
    'used': True,
    'keyhashed': 'crc',
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '!%5v(-gnc%t3=3*%q_8l-00ptauveh%t3712p%sfh^8&5+qs_j'

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz")

ROOT_URLCONF = 'django_rediscache_test.urls'

TEMPLATE_DIRS = tuple()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'app',
    'django_rediscache',
)

CACHE_USE = True

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:0',
    }
}

from logging.handlers import SysLogHandler

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(name)s %(pathname)s:%(lineno)d %(message)s'
            },
        'simple': {
            'format': '%(levelname)s %(message)s'
            },
        'console_formatter': {
            'format': (
                '\x1b[37;40m[%(asctime)s] '
                '\x1b[36;40m%(levelname)8s '
                '%(name)s '
                '\x1b[32;40m%(filename)s'
                '\x1b[0m:'
                '\x1b[32;40m%(lineno)d '
                '\x1b[33;40m%(message)s\x1b[0m')
            }
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
            },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'facility': SysLogHandler.LOG_LOCAL2,
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'syslog'],
            'level': 'WARNING',
            'propagate': True
            },
        'django_rediscache': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
            },
        },
}
