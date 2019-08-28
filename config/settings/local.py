from .base import *


DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost',
                 '0.0.0.0', 'f5af3bea.ngrok.io']


INSTALLED_APPS += [
    'django_extensions',
]
