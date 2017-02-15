from datetime import datetime
from fruitfam import db

class RequestLog(db.Model):
  __tablename__ = "request_logs"
  id = db.Column(db.Integer, primary_key = True)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
      backref=db.backref("request_logs"))
  
  url = db.Column(db.String(511))
  ip = db.Column(db.String(255))
  env = db.Column(db.String(255))
  request_time = db.Column(db.DateTime)
  ms_taken = db.Column(db.Float)

  def __init__(self, url, user, ip, env, ms_taken, created=None):
      self.url = url
      self.user = user
      self.ip = ip
      self.env = env
      self.ms_taken = ms_taken
      if created is None:
        created = datetime.utcnow()
      self.request_time = created

  def __repr__(self):
    return '<RequestLog %r>' % self.id