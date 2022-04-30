from env import DB_USER, DB_PASSWORD
from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-^t!eh64gj_=lh4eatz$rng#^s#n1$!k-(%$s#wtzm9$i0@0(l!'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cse_archive',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
    }
}
