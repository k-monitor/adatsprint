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

ADMINS = MANAGERS = [
    ('Baptiste Mispelon', 'bmispelon@gmail.com'),
]

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'bmispelon@gmail.com'
with open('/home/adatozz/DJANGO_EMAIL_HOST_PASSWORD') as f:
    EMAIL_HOST_PASSWORD = f.read().strip()
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[Adatozz] '
SERVER_EMAIL = 'adatozz@mispelon.eu'

INSTALLED_APPS += ('opbeat.contrib.django',)
OPBEAT = {
    'ORGANIZATION_ID': '0d084279d6844a2a82ec28d2092d309a',
    'APP_ID': '9686aa7f10',
}
with open('/home/adatozz/DJANGO_OPBEAT_SECRET_TOKEN') as f:
    OPBEAT['SECRET_TOKEN'] = f.read().strip()
MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
) + MIDDLEWARE_CLASSES
