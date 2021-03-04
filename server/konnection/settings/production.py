

from konnection.settings.base import *
import os
import dj_database_url


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = 'TEMPORARY_KEY'


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
