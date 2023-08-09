import os
from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-beqx(l-u0_s2(%7&$jsq6o_5_$j@l_q+g9val&=tx_2f*ze4zn'

ALLOWED_HOSTS = ['localhost']

# Allow cross origins
# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
  'http://localhost:8100',
  'http://127.0.0.1:8100',
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fyp',
        'HOST': '172.26.0.1',
        'USER': 'root',
        'PASSWORD': 'root'
    }
}