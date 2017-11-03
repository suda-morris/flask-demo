# encoding:utf-8
import os

DEBUG = False

DIALECT = "sqlite"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASEDIR, 'data.sqlite')
SQLALCHEMY_DATABASE_URI = "{}:///{}".format(DIALECT, DATABASE)
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
