from datetime import datetime, timedelta

from fruitfam import db

class UserMission(db.Model):
  __tablename__ = 'user_missions'
  id = db.Column(db.Integer, primary_key = True)
  created = db.Column(db.DateTime)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
    backref=db.backref('user_missions'))
  
  is_over = db.Column(db.Boolean, default = False)
  mission_id = db.Column(db.Integer)
  booty = db.Column(db.Integer)
  
  def __init__(self, user, mission_id, created=None):
    
    self.user = user
    self.mission_id = mission_id
    if created is None:
      created = datetime.utcnow()
    self.created = created
  
  def __repr__(self):
    return 'something with the rules...'