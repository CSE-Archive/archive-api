from dj_database_url import config

from .common import *


ALLOWED_HOSTS = ['cse-archive.herokuapp.com']

DATABASES = {
    'default': config()
}
