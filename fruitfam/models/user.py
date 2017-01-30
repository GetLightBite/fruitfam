from itsdangerous import (JSONWebSignatureSerializer
              as Serializer, BadPayload, BadHeader, BadSignature)
from datetime import datetime, timedelta, date
from fruitfam import app, db
from sqlalchemy.orm import joinedload, subqueryload, joinedload_all, load_only
from sqlalchemy import desc, or_, not_, and_

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(80), index = True)
  lastname = db.Column(db.String(80), index = True)
  email = db.Column(db.String(120), unique=True)
  token = db.Column(db.String(255))
  joined = db.Column(db.DateTime)
  profile_photo = db.Column(db.String(255))
  utc_offset = db.Column(db.Integer)
  streak = db.Column(db.Integer)
  last_log = db.Column(db.DateTime)
  fb_id = db.Column(db.String(255))
  
  # send_notifications = db.Column(db.Boolean, default = True)
  # apns_token = db.Column(db.String(255))
  # phone_number = db.Column(db.String(127))
  # latest_version = db.Column(db.String(127))
  # booty = db.Column(db.Integer)
  # level = db.Column(db.Integer)
  # last_latitude = db.Column(db.Float)
  # last_longitude = db.Column(db.Float)
  # birthday = db.Column(db.DateTime)
  # gender = db.Column(db.Integer)
  # diet_type = db.Column(db.Integer)
  # goals = db.Column(db.Integer)
  # is_anonymous = db.Column(db.Integer, default=False)
  # is_fake = db.Column(db.Boolean, default = False)

  def __init__(self, firstname, lastname, email, joined = None):
    self.email = email
    self.firstname = firstname
    self.lastname = lastname
    self.streak = 0
    if joined is None:
      joined = datetime.utcnow()
    self.joined = joined

  def __repr__(self):
    return '<User %r>' % (self.real_name())
  
  def get_last_log_local(self):
    return self.last_log + timedelta(hours=self.last_timezone())
  
  def generate_auth_token(self):
    s = Serializer(app.config['SECRET_KEY'])
    token_data = {
      'id': self.id, 
      'created': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
    print token_data
    token = s.dumps(token_data)
    print 'token'
    print token
    self.token = token
    db.session.add(self)
    db.session.commit()
    return token

  def name(self):
    return self.real_name()
  
  def get_firstname(self):
    if self.firstname == None:
      return ''
    return self.firstname
  
  def get_lastname(self):
    if self.lastname == None:
      return ''
    return self.lastname
  
  def real_name(self):
    if self.firstname == None or self.lastname == None:
      return ''
    return self.firstname + " " + self.lastname
  
  def initials(self):
    if self.firstname in [None, ''] or self.lastname in [None, '']:
      return ''
    return self.firstname.upper()[0] + self.lastname.upper()[0]
  
  def last_timezone(self):
    if self.utc_offset == None:
      return -8
    return self.utc_offset
  
  @staticmethod
  def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
    except BadPayload:
      return None # Couldnt decode
    except BadHeader:
      return None # Malformed header
    except BadSignature as b:
      print b
      return None
    user = User.query.get(data[kId])
    return user
  
  @staticmethod
  def create_user(firstname, lastname, email):
    user = User(firstname, lastname, email)
    db.session.add(user)
    db.session.commit()
    token = user.generate_auth_token()
    return (user, token)