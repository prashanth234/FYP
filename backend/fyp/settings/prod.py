import os
from .common import *

DEBUG = False

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = 'django-insecure-beqx(l-u0_s2(%7&$jsq6o_5_$j@l_q+g9val&=tx_2f*ze4zn'

# List of hosts that are allowed to serve your application
ALLOWED_HOSTS = ['localhost']

CORS_ORIGIN_ALLOW_ALL = False

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