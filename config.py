AUTHY_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
SECRET_KEY = 'any key of your choice'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
