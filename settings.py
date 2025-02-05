import os
import string

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400
HTTP_SERVER_ERROR = 500
MAX_SHORT_LEN = 16
MAX_GENERATED_LEN = 6
MAX_ORIGINAL_LEN = 1000
CHARACTERS = (string.ascii_uppercase +
              string.ascii_lowercase + string.digits)
INDEX = 'index_view'
ITERATIONS = 100


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
