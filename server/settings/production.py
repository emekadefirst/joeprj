import os
from .base import *
from datetime import timedelta


ALLOWED_HOSTS = ['*']

SECRET_KEY = 'django-insecure-^h%1ius-)i(8jgpj4hamg_r)7w47ikkg&8g+^$4lmg3pgie#a2'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": 5432,
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5173",
]


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=14),  
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),  
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # For production, consider using Redis:
        # 'BACKEND': 'django_redis.cache.RedisCache',
        # 'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}