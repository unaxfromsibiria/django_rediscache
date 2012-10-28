DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_rediscache_test',
        'USER': 'root',
        'PASSWORD': 'pypassw0rd',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

TIME_ZONE = 'Asia/Novosibirsk'
LANGUAGE_CODE = 'ru'

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'b#$qr)wh-^9@t1$4uugy=wt5d-&amp;pt#jpdv#-s&amp;mkiil&amp;x%2g0@'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
                  'test_application',
                  'django_rediscache', 
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DJANGO_REDISCACHE = {
    'scheme' : {'test_application.models.Model1' : {'all' : 3600},
                'test_application.models.Model2' : {'all' : 3600},
                'test_application.models.Model3' : {'all' : 3600},
                },
    'redis' : {
        'host': 'localhost',
        'port': 6379,
        'db'  : 2,
        'socket_timeout': 5,
    },
    'used'      : True,
    'keyhashed' : 'crc',
}
