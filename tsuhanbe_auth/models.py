# -*- coding: utf-8 -*-
# tsuhanbe_auth.models

from google.appengine.ext import db
from kay.auth.models import GoogleUser

# Create your models here.

class User(GoogleUser):
    pass