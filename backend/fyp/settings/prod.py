import os
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fyp',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root'
    }
}