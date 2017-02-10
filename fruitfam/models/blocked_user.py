from datetime import datetime
from fruitfam import db

class BlockedUser(db.Model):
  __tablename__ = 'blocked_users'
  id = db.Column(db.Integer, primary_key = True)
  
  blocking_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  blocking_user = db.relationship('User',
    backref=db.backref('blocked_users'),
    foreign_keys='BlockedUser.blocking_user_id')
  
  blocked_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  blocked_user = db.relationship('User',
    backref=db.backref('blocked_by_users'),
    foreign_keys='BlockedUser.blocked_user_id')
  
  created = db.Column(db.DateTime)

  def __init__(self, blocking_user_id, blocked_user_id, created=None):
    self.blocking_user_id = blocking_user_id
    self.blocked_user_id = blocked_user_id
    if created is None:
      created = datetime.utcnow()
    self.created = created

  def __repr__(self):
    return '<BlockedUser -  %r blocked %r>' % (self.blocking_user_id, self.blocked_user_id)