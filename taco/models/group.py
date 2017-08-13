from datetime import datetime
from taco import app, db
from sqlalchemy.orm import joinedload, subqueryload, joinedload_all, load_only
from sqlalchemy import desc, or_, not_, and_

class Group(db.Model):
  __tablename__ = 'groups'
  id = db.Column(db.Integer, primary_key = True)
  
  group_name = db.Column(db.String(255), index = True) # 100x100 = db.Column(db.String(255))
  admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  admin = db.relationship('User', backref=db.backref('groups'))
  
  created = db.Column(db.DateTime)
  
  def __init__(self, group_name, admin, joined = None):
    self.group_name = group_name
    self.admin = admin
    self.admin_id = admin.id
    if joined is None:
      joined = datetime.utcnow()
    self.joined = joined

  def __repr__(self):
    return '<Group %d>' % (self.id)