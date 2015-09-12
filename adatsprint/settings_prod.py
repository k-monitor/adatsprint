import os

from adatsprint.settings import *

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

ADMINS = MANAGERS = [
    ('Baptiste Mispelon', 'bmispelon@gmail.com'),
]

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'bmispelon@gmail.com'
with open('/home/adatozz/DJANGO_EMAIL_HOST_PASSWORD') as f:
    EMAIL_HOST_PASSWORD = f.read().strip()
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[adatsprint] '
SERVER_EMAIL = 'adatsprint@mispelon.eu'
