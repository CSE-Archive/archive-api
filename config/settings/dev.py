import os

from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-^t!eh64gj_=lh4eatz$rng#^s#n1$!k-(%$s#wtzm9$i0@0(l!'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'cse_archive'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
    }
}
