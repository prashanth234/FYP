import os
from .common import *

DEBUG = False

SECRET_KEY = os.environ.setdefault('SECRET_KEY', 'django-insecure-beqx(l-u0_s2(%7&$jsq6o_5_$j@l_q+g9val&=tx_2f*ze4zn')

# List of hosts that are allowed to serve your application
ALLOWED_HOSTS = os.environ.setdefault('FYP_ALLOWED_HOSTS', 'localhost').split(',') 

CORS_ORIGIN_ALLOW_ALL = False

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.setdefault('MYSQL_DBNAME', 'fyp'),
        'HOST': os.environ.setdefault('MYSQL_HOST', 'mysql_db'),
        'USER': os.environ.setdefault('MYSQL_USER', 'fypuser'),
        'PASSWORD': os.environ.setdefault('MYSQL_PASSWORD', 'fyppass'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True, 
        }
    }
}

ENABLE_FIREBASE=True

STORAGES = {
  "default": {
    "BACKEND": "fyp.customStorage.CustomS3Storage",
    "OPTIONS": {
      "access_key": os.environ.get('AWS_S3_ACCESS_KEY_ID'),
      "secret_key": os.environ.get('AWS_SECRET_ACCESS_KEY'),
      "bucket_name": os.environ.get('AWS_STORAGE_BUCKET_NAME'),
      "region_name": os.environ.get('AWS_S3_REGION_NAME'),
      "endpoint_url": os.environ.get('AWS_S3_ENDPOINT_URL'),
      "addressing_style": "virtual",
      "file_overwrite": False
    }
  },
  "staticfiles": {
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
  }
}