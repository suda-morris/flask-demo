# encoding:utf-8
import os
from datetime import timedelta

DEBUG = False

SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

DIALECT = "sqlite"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASEDIR, 'app.sqlite')
SQLALCHEMY_DATABASE_URI = "{}:///{}".format(DIALECT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

MQTT_BROKER_URL = "192.168.1.106"
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = "sub_client"
MQTT_PASSWORD = "321woaini"
MQTT_REFRESH_TIME = 1.0
