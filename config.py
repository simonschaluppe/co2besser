import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'alintschi'
    # SQLALCHEMY_DATABASE_URI = "sqlite:////db/db.sqlite"
    FLASK_DEBUG = 1
    SQLALCHEMY_ECHO = True
