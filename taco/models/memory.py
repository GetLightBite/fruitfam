from datetime import datetime
from taco import app, db
from sqlalchemy.orm import joinedload, subqueryload, joinedload_all, load_only
from sqlalchemy import desc, or_, not_, and_

class Memory(db.Model):
  __tablename__ = 'memories'
  id = db.Column(db.Integer, primary_key = True)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', backref=db.backref('memories'))
  
  group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
  group = db.relationship('Group', backref=db.backref('memories'))
  
  url_icon = db.Column(db.String(255), index = True) # 240x240
  url_small = db.Column(db.String(255), index = True) # 414x587
  url_fullscreen = db.Column(db.String(255), index = True) # 720x?
  
  width = db.Column(db.Integer)
  height = db.Column(db.Integer)
  url_original = db.Column(db.String(255), index = True)
  
  memory_type = db.Column(db.String(80), index = True)
  
  created = db.Column(db.DateTime)
  
  def __init__(self, user, group, url_icon, url_small, url_fullscreen, width , height, url_original, memory_type, created = None):
    self.user = user
    self.user_id = user.id
    self.group = group
    self.group_id = group.id
    self.url_icon = url_icon
    self.url_small = url_small
    self.url_fullscreen = url_fullscreen
    self.width = width
    self.height = height
    self.url_original = url_original
    self.memory_type = memory_type
    if created is None:
      created = datetime.utcnow()
    self.created = created

  def __repr__(self):
    return '<Memory %d by user %d>' % (self.id, self.user_id)