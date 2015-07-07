import os

from adatozz.settings import *

DEBUG = False

ALLOWED_HOSTS = ['adatsprint.k-monitor.hu']

with open('/home/adatozz/DJANGO_SECRET_KEY') as f:
    SECRET_KEY = f.read()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'adatozz',
    }
}

STATIC_ROOT = '/home/adatozz/collected_static/'
MEDIA_ROOT = '/home/adatozz/uploads/'
MEDIA_URL = '/uploads/'
