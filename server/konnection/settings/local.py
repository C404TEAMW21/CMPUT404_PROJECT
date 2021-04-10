from pathlib import Path

from konnection.settings.base import *
import os
import dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Adding secrets to env file
# From StackOverflow https://stackoverflow.com/a/61437799
# From Zack Plauché https://stackoverflow.com/users/10415970/zack-plauch%c3%a9
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'TEMPORARY_KEY'

# Connecting PostgreSQL to Django
# From https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
# From Digital Ocean
# From Justin Ellingwood https://www.digitalocean.com/community/users/jellingwood
if os.getenv('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github-actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'myproject',
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# For tests
# https://stackoverflow.com/a/35224204
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-spec', '--spec-color']
