import os
from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-beqx(l-u0_s2(%7&$jsq6o_5_$j@l_q+g9val&=tx_2f*ze4zn'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Allow cross origins
CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = [
  # 'http://localhost:8100'
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'fyp_prod_clone2',
    'HOST': 'localhost',
    'USER': 'root',
    'PASSWORD': 'root',
    'OPTIONS': {
      'charset': 'utf8mb4',
      'use_unicode': True, 
    }
  }
}

ENABLE_FIREBASE=False

# STORAGES = {
#   "default": {
#     "BACKEND": "fyp.customStorage.CustomS3Storage",
#     "OPTIONS": {
#       "access_key": os.environ.get('AWS_S3_ACCESS_KEY_ID'),
#       "secret_key": os.environ.get('AWS_SECRET_ACCESS_KEY'),
#       "bucket_name": os.environ.get('AWS_STORAGE_BUCKET_NAME'),
#       "region_name": os.environ.get('AWS_S3_REGION_NAME'),
#       "endpoint_url": os.environ.get('AWS_S3_ENDPOINT_URL'),
#       "addressing_style": "virtual",
#       "file_overwrite": True
#     }
#   },
#   "staticfiles": {
#     "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#   }
# }

# Pacakge required by s3
# boto3 = "*"
# django-storages = "*"

# Pacakge required by celery
# redis = "*"
# celery = "*"
# Celery configuration
# CELERY_BROKER_URL = 'redis://localhost:6379/1'
