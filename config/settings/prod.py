import os

from .common import *
from dj_database_url import config


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['cse-archive.herokuapp.com']

DATABASES = {
    'default': config()
}
