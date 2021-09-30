
from configparser import ConfigParser
import os

configdir = '/'.join([os.path.dirname(os.path.realpath(__file__)),'config.ini'])

config = ConfigParser()
config.read(configdir)

class Config:
    SECRET_KEY = config['csrf']['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config['SQLAlchemy']['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ECHO = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = 0
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = config['gmail']['USER_MAIL']
    MAIL_PASSWORD = config['gmail']['USER_PASS']
