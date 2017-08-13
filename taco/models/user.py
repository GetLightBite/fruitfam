from itsdangerous import (JSONWebSignatureSerializer
              as Serializer, BadPayload, BadHeader, BadSignature)
from datetime import datetime, timedelta, date
from taco import app, db
from sqlalchemy.orm import joinedload, subqueryload, joinedload_all, load_only
from sqlalchemy import desc, or_, not_, and_

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255), index = True)
  phone_number = db.Column(db.String(80), index = True)
  token = db.Column(db.String(255))
  joined = db.Column(db.DateTime)
  apns_token = db.Column(db.String(255))
  send_notifications = db.Column(db.Boolean, default = True)
  
  def __init__(self, username, phone_number, joined = None):
    self.username = username
    self.phone_number = phone_number
    if joined is None:
      joined = datetime.utcnow()
    self.joined = joined

  def __repr__(self):
    return '<User %r>' % (self.real_name())
  
  def is_founder(self):
    if self.fb_id != None:
      return self.fb_id in ['10155199004034095', '10211735004991165']
      return True
    return False
  
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

  def get_username(self):
    return self.username
  
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
  def create_user(username, phone_number):
    existing_user = User.query.filter_by(
      username=username
    ).filter_by(
      phone_number=phone_number
    ).first()
    if existing_user != None:
      return (None, None)
    user = User(username, phone_number)
    db.session.add(user)
    db.session.commit()
    token = user.generate_auth_token()
    return (user, token)