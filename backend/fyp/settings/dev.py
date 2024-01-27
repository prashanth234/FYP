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
    'NAME': 'fyp_1',
    'HOST': 'localhost',
    'USER': 'root',
    'PASSWORD': 'root',
    'OPTIONS': {
      'charset': 'utf8mb4',
      'use_unicode': True, 
    }
  }
}

# DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
# # STATICFILES_STORAGE = "storages.backends.s3.S3Storage"

# AWS_S3_ACCESS_KEY_ID = "AKIA3KJ5UR7V3YUG6HHK"
# AWS_SECRET_ACCESS_KEY = "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"
# AWS_STORAGE_BUCKET_NAME = "fypassets"
# AWS_S3_REGION_NAME = "ap-south-1"

# Pacakge required by s3
# boto3 = "*"
# django-storages = "*"