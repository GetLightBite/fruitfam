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
  gender = db.Column(db.String(80), index = True)
  email = db.Column(db.String(120), unique=True)
  token = db.Column(db.String(255))
  joined = db.Column(db.DateTime)
  profile_photo = db.Column(db.String(255))
  utc_offset = db.Column(db.Integer)
  streak = db.Column(db.Integer)
  max_streak = db.Column(db.Integer)
  last_log = db.Column(db.DateTime)
  fb_token = db.Column(db.String(255))
  fb_id = db.Column(db.String(255))
  
  # booty = db.Column(db.Integer)
  level = db.Column(db.Integer)
  
  # send_notifications = db.Column(db.Boolean, default = True)
  # apns_token = db.Column(db.String(255))
  # phone_number = db.Column(db.String(127))
  # latest_version = db.Column(db.String(127))
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
  
  def get_profile_photo(self):
    if self.profile_photo == None:
      return 'https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-1/c349.149.312.312/s160x160/11161343_10153393544189095_5097894419925828650_n.jpg?oh=c0d181176fb41051a0022ae20ba9034c&oe=5946493C'
    return self.profile_photo
  
  def get_level(self):
    if self.level == None:
      return 1
    return self.level
  
  # def get_booty(self):
  #   if self.booty == None:
  #     return 0
  #   return self.booty
  
  def get_streak(self):
    if self.streak == None:
      return 0
    return self.streak
  
  def get_streak(self):
    if self.streak == None:
      return 0
    return self.streak
  
  def get_max_streak(self):
    if self.max_streak == None:
      return 0
    return self.max_streak
  
  def get_last_log_local(self):
    last_log = self.last_log
    last_timezone = self.last_timezone()
    if last_log == None:
      last_log = datetime(2017, 1, 1)
    print last_log
    return last_log + timedelta(hours=last_timezone)
  
  def local_time(self):
    now = datetime.utcnow()
    last_timezone = self.last_timezone()
    return now + timedelta(hours=last_timezone)
  
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
      return 'AbhinavTest'
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
    user = User.query.get(data['id'])
    return user
  
  @staticmethod
  def create_user(firstname, lastname, email, fb_token=None, fb_id=None):
    user = User(firstname, lastname, email)
    user.fb_token = fb_token
    user.fb_id = fb_id
    db.session.add(user)
    db.session.commit()
    token = user.generate_auth_token()
    return (user, token)