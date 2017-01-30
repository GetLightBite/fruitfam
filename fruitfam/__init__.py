from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config')

# Extensions
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

import fruitfam.views.core

### Error handlers go here