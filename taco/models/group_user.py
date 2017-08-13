from datetime import datetime
from taco import app, db
from sqlalchemy.orm import joinedload, subqueryload, joinedload_all, load_only
from sqlalchemy import desc, or_, not_, and_

class GroupUser(db.Model):
  __tablename__ = 'group_users'
  id = db.Column(db.Integer, primary_key = True)
  
  group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
  group = db.relationship('Group', backref=db.backref('group_users'))
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', backref=db.backref('group_users'))
  
  created = db.Column(db.DateTime)
  
  def __init__(self, group, user, joined = None):
    self.group = group
    self.group_id = group.id
    self.user = user
    self.user_id = user.id
    if joined is None:
      joined = datetime.utcnow()
    self.created = joined

  def __repr__(self):
    return '<GroupUser %d, group: %d, user: %d>' % (self.id, self.group_id, self.user_id)