import os
import string
import re


MAX_SHORT_LEN = 16
MAX_GENERATED_LEN = 6
MAX_ORIGINAL_LEN = 1000
CHARACTERS = (string.ascii_uppercase +
              string.ascii_lowercase + string.digits)
REGEX = f"^[{re.escape(CHARACTERS)}]+$"
ITERATIONS = 100


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
