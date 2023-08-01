import os
from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-beqx(l-u0_s2(%7&$jsq6o_5_$j@l_q+g9val&=tx_2f*ze4zn'

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