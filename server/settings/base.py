import os
from . import env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # installed packages
    "rest_framework_simplejwt",
    "drf_yasg",
    "rest_framework",
    "corsheaders",
    # apps
    'user',
    'api',
    'zaudit',
]

AUTHENTICATION_BACKENDS = [
    "user.backend.CustomBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "user.User"

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = ["static"]
STATIC_ROOT = "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join("media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND = env.EMAIL_BACKEND
EMAIL_HOST = env.EMAIL_HOST
EMAIL_PORT = env.EMAIL_PORT
EMAIL_USE_SSL = env.EMAIL_USE_SSL
EMAIL_USE_TLS = env.EMAIL_USE_TLS
EMAIL_HOST_USER = env.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = env.EMAIL_HOST

