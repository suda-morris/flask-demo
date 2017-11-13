# encoding: utf-8

from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt

db = SQLAlchemy()
mqtt = Mqtt()
