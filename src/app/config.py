import os

SQLALCHEMY_DATABASE_URI = DATABASE_URL = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
