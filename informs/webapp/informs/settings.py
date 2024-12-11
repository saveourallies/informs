"""
Django settings for informs project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-))gr)koo$_$jilzn-gcqe!q82%s&ce6de*vxu7@#rc4#j_0!l5'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('DJANGO_DEBUG') == 'False':
    DEBUG = False
else:
    DEBUG = True

SERVERNAME1 = os.environ.get('SERVERNAME1')
SERVERNAME2 = os.environ.get('SERVERNAME2')

ALLOWED_HOSTS = ["127.0.0.1", SERVERNAME1, SERVERNAME2]

SITE_ID = 1

CSRF_TRUSTED_ORIGINS = [
    'https://' + SERVERNAME1,
    'https://' + SERVERNAME2,
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    # 'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap_icons',
    'django_q',
    'auditlog',
    'tz_detect',
    'crispy_forms',
    'crispy_bootstrap5',
    'mathfilters',
    'accounts.apps.AccountsConfig',
    'aidrequests.apps.AidRequestsConfig',
    'takserver.apps.TakServerConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'informs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['informs/templates', 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'aidrequests.context_processors.fieldops_active'
            ],
        },
    },
]

WSGI_APPLICATION = 'informs.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

SQLITE_FILE = os.environ.get('SQLITE_FILE')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': SQLITE_FILE
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = '/opt/app/static_files/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Template Pack
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_COOKIE_AGE = 1 * 24 * 60 * 60  # 1 day cookie
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 500

BOOTSTRAP5 = {
    "css_url": {
        "href": "{% static 'css/custom-bootstrap.css' %}",  # your custom CSS file
    },
}
LOGIN_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
    # ...
}

# Email Setup
MAIL_FROM_DOMAIN = os.environ.get('MAIL_FROM_DOMAIN')
MAIL_FROM_USER = os.environ.get('MAIL_FROM_USER')
MAIL_FROM_KEY = os.environ.get('MAIL_FROM_KEY')
MAIL_FROM = f'{MAIL_FROM_USER}@{MAIL_FROM_DOMAIN}'
MAIL_TO_TEST = os.environ.get('MAIL_TO_TEST')
MAIL_ENDPOINT = os.environ.get('MAIL_ENDPOINT')

# MAPS
AZURE_MAPS_KEY = os.environ.get('AZURE_MAPS_KEY')

# TAK Server
TAKSERVER_DNS = os.environ.get('TAKSERVER_DNS')
PYTAK_TLS_CLIENT_CERT = os.environ.get('PYTAK_TLS_CLIENT_CERT')
PYTAK_TLS_CLIENT_PASSWORD = os.environ.get('PYTAK_TLS_CLIENT_PASSWORD')
PYTAK_TLS_CLIENT_CAFILE = os.environ.get('PYTAK_TLS_CLIENT_CAFILE')

Q_CLUSTER = {
    'name': 'informs-queuy',
    'label': 'queues',
    'workers': 1,
    'orm': 'default',
    'retry': 120,
    'timeout': 60,
    'recycle': 500
}