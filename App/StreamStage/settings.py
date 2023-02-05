"""
Django settings for StreamStage project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from .secrets import DJANGO_SECRET_KEY, SENDGIRD_TOKEN

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'www.streamstage.co',
    'me.streamstage.co',
    'streamstage.co',
    'master.streamstage.co',
]

CSRF_TRUSTED_ORIGINS = [
    'https://me.streamstage.co',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.+$",
]

DEFAULT_HOST = 'www'

ROOT_HOSTCONF = 'StreamStage.hosts'
ROOT_URLCONF = 'StreamStage.urls'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local
    'accounts',
    'server_manager',
    'events',

    # 3rd Party
    'crispy_forms',
    # 'corsheaders',
    'crispy_bootstrap5',
    'rest_framework',
    'django_hosts',
    'stripe',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'StreamStage.urls'


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
MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))


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

# Stripe keys
# STRIPE_SECRET_KEY = ''
# STRIPE_PUBLISHABLE_KEY = ''

INBOUND_EMAIL = 'inquiries@StreamStage.co'
OUTBOUND_EMAIL = 'mail@streamstage.co'

# DEV Key
SENDGIRD_TOKEN = SENDGIRD_TOKEN