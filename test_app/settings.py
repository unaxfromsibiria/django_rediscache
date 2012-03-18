# Django settings for django_rediscache project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (,)

MANAGERS = ADMINS

DATABASES = {
    'default' : {
    'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
    'NAME'    : 'django_rediscache',
    'USER'    : 'admin',
    'PASSWORD': '*****',
    'HOST'    : 'localhost',
    'PORT'    : '5432',
    },
}

TIME_ZONE = 'Asia/Novosibirsk'

LANGUAGE_CODE = 'ru'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (

)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n8^_gfhw7uqz!h$n5e3a(#i!q@+n3krngsu$wkt9a2-3jgxh6='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'


DJANGO_REDISCACHE = {
    'scheme' : {'test_app.TestModel1' : { 'list' : 1200, 'count' : 1200, 'get' : 1800 },
                'test_app.TestModel2' : { 'all' : 1200 },
                'test_app.TestModel3' : { 'all' : 1200 },
               },
    'redis' : {
        'host': 'localhost',
        'port': 6379,
        'db'  : 2,
        'socket_timeout': 5,
    },               
    'used' : False,
    'keyhashed' : True,
}

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_rediscache',
    'test_app',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
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
