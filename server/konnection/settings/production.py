from konnection.settings.base import *
import os
import dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Adding secrets to env file
# From StackOverflow https://stackoverflow.com/a/61437799
# From Zack Plauché https://stackoverflow.com/users/10415970/zack-plauch%c3%a9
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


# SECURITY WARNING: don't turn it to True!
DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
