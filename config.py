# encoding:utf-8
import os
from datetime import timedelta

DEBUG = True

SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

DIALECT = "sqlite"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASEDIR, 'app.sqlite')
SQLALCHEMY_DATABASE_URI = "{}:///{}".format(DIALECT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
