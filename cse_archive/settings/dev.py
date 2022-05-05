import os

from env import DB_USER, DB_PASSWORD, JSON_CONTENTS
from .common import *


os.environ.setdefault("GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS", JSON_CONTENTS)


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

GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None
