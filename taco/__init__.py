from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')

# Extensions
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

from celery import Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(
  CELERY_ACCEPT_CONTENT  = ['pickle'],
  CELERY_TASK_SERIALIZER = 'pickle',
  CELERY_RESULT_SERIALIZER = 'pickle'
)

import taco.views.core

### Error handlers go here