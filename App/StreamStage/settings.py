"""
Django settings for StreamStage project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import CloudFlare
from .secrets import DJANGO_SECRET_KEY, SENDGIRD_TOKEN, CLOUDFLARE_TOKEN

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SET THIS TO TRUE IF YOU ARE USING LOCALHOST
# IF THIS IS TRUE, COOKIES WONT WORK (SESSIONS WONT WORK)
# AND REVERSE'S WONT WORK
RUNNING_ON_LOCALHOST = False

if os.path.isfile("./.localhost"):
    RUNNING_ON_LOCALHOST = True
    print("Found .localhost file, server settings adjusted accordingly.")

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.0.227',
    'streamstage.co',
    '.streamstage.co',
]

CERT_DIR = str(BASE_DIR / 'certs')

#
# Cloudflare
#
DOMAIN_NAME = 'streamstage.co'
# Set to False if you don't use Cloudflare
# As this will dictate if domain DNS is updated.
# If its True and you don't use Cloudflare, 
# you will get an error and the node wont be able to start.
USE_CLOUDFLARE = True

acf = None
if USE_CLOUDFLARE:
    acf = CloudFlare.CloudFlare(token=CLOUDFLARE_TOKEN)



#
# Subdomains
#
DEFAULT_HOST = 'www'
ROOT_HOSTCONF = 'StreamStage.hosts'
ROOT_URLCONF = 'StreamStage.urls'

if RUNNING_ON_LOCALHOST == False:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_DOMAIN = ".streamstage.co"
    SESSION_COOKIE_DOMAIN = ".streamstage.co"
    CSRF_COOKIE_SAMESITE = 'None'

elif RUNNING_ON_LOCALHOST == True:
    SESSION_COOKIE_SECURE = False

#
# CSRF / CORS
# 
CSRF_TRUSTED_ORIGINS = [
    'https://me.streamstage.co',
    'https://streamstage.co',
    'https://applications.streamstage.co',
    'https://events.streamstage.co',
    'https://search.streamstage.co',
    'https://store.streamstage.co',
    'https://orders.streamstage.co',
    'https://www.streamstage.co',
    'https://master.streamstage.co',
    'https://localhost:8000',
]

X_FRAME_OPTIONS = 'ALLOW-FROM *://*.streamstage.co/*'
CORS_ALLOWED_ORIGIN_REGEXES = [r"^https://.+$"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
    'streamstage-token',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

#
# Application definition
#
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Local
    'accounts',
    'events',
    'applications',
    'search',
    'store',
    'orders',
    'homepage',
    'StreamStage',

    # 3rd Party
    'crispy_forms',
    'webpack_loader',
    'corsheaders',
    'annoying',
    'crispy_bootstrap5',
    'django_countries',
    'rest_framework',
    'django_hosts',
    'stripe',
]

WEBPACK_LOADER = {
  'DEFAULT': {
    'CACHE': not DEBUG,
    'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    'POLL_INTERVAL': 0.1,
    'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
  }
}

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    'accounts.com_lib.api_session_middleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'StreamStage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Developer Content
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('staticfiles'))]
STATIC_ROOT = str(BASE_DIR.joinpath('static'))
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# User-uploaded content
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))
MEDIA_URL = 'media/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User
AUTH_USER_MODEL = 'accounts.Member'

# Login & Logout redirects
# LOGIN_REDIRECT_URL = 'member_profile'
# LOGOUT_REDIRECT_URL = ''

# Bootstrap & Django forms
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Password reset email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
INBOUND_EMAIL = 'inquiries@StreamStage.co'
OUTBOUND_EMAIL = 'mail@streamstage.co'
SUPPORT_EMAIL = 'help@streamstage.co'

# DEV Key
SENDGIRD_TOKEN = SENDGIRD_TOKEN


# Key TTL's
EMAIL_VERIFICATION_TTL = 60 * 24 * 2