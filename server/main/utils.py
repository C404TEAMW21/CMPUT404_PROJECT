"""main user model Configuration
This file is used to store static varible and enums
to be used for main user model
"""

from enum import Enum
from django.conf import settings

HOST = "https://konnection-server.herokuapp.com/"
FRONTEND_HOST = "https://konnection-client.herokuapp.com"

class UserType(Enum):
    superuser = 'superuser'
    author = 'author'