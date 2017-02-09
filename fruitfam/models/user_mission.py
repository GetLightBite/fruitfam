from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.missions.actions import get_users_rules

class UserMission(db.Model):
  __tablename__ = 'user_missions'
  id = db.Column(db.Integer, primary_key = True)
  created = db.Column(db.DateTime)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
    backref=db.backref('user_missions'))
  
  is_over = db.Column(db.Boolean, default = False)
  mission_id = db.Column(db.Integer)
  booty = db.Column(db.Integer, default=0)
  
  timeouts_reached = db.Column(db.Integer, default=0)
  
  def __init__(self, user, mission_id, created=None):
    
    self.user = user
    self.mission_id = mission_id
    if created is None:
      created = datetime.utcnow()
    self.created = created
    
    # Schedule notifications
    rules = self.get_rules()
    rules.schedule_notifs()
  
  def get_booty(self):
    if self.booty == None:
      return 0
    return self.booty
  
  def increment_booty(self, booty):
    self.booty = self.get_booty() + booty
  
  def get_timeouts_reached(self):
    if self.timeouts_reached == None:
      return 0
    return self.timeouts_reached
  
  def increment_timeouts_reached(self):
    self.timeouts_reached = self.get_timeouts_reached() + 1
  
  def get_rules(self):
    return get_users_rules(self)
  
  def end_mission(self):
    self.is_over = True
    user = self.user
    if user.level == None:
      user.level = 1
    user.level += 1
    new_mission = UserMission(user, self.mission_id+1)
    db.session.add(new_mission)
    return new_mission
  
  def __repr__(self):
    return 'something with the rules...'