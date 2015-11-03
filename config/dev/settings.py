"""
Database credentials should be exported to the ENV.
There are defaults here that can be overridden.
"""
import os
from colorlog import ColoredFormatter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '097zz(^_!me*&3eb1j1)v5)44du#!i#i2))7&yc_&5z^-(Ea@8')

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'elections_admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'elections_admin.urls'

WSGI_APPLICATION = 'config.dev.app.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PYSCOTUS_DB_NAME', 'elex'),
        'USER': os.environ.get('PYSCOTUS_DB_USER', 'elex'),
        'PASSWORD': os.environ.get('PYSCOTUS_DB_PASSWORD', ''),
        'HOST': os.environ.get('PYSCOTUS_DB_HOST', ''),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

TEMPLATE_DIRS = (
    'elections_admin/templates/',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s %(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple_console': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s %(levelname)s %(message)s',
        },
        'simple_file': {
            'format': '%(asctime)s jeremy_laptop elections-2016: %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple_file',
        },
        'syslog':{
          'level': 'INFO',
          'class': 'logging.handlers.SysLogHandler',
          'formatter': 'simple_file',
          'address': (os.environ.get('ELEX_LOGGING_URL', 'logs2.papertrailapp.com'), int(os.environ.get('ELEX_LOGGING_PORT', 21)))
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}