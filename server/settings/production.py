import os
from .base import *
from datetime import timedelta
from . import env

ALLOWED_HOSTS = ['admin.rccgdailymanuals.com']

SECRET_KEY = env.SECRET_KEY

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
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.DATABASE_NAME,
        'USER': env.DATABASE_USER,
        'PASSWORD': env.DATABASE_PASSWORD,
        'HOST': 'localhost'
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://admin.rccgdailymanuals.com",
    'https://admin-hazel-xi.vercel.app',
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