import os

database_url = os.getenv('DATABASE_URI')

class TestConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
