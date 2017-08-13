from datetime import datetime
from taco import db

class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
    backref=db.backref('comments'))
  
  memory_id = db.Column(db.Integer, db.ForeignKey('memories.id'))
  memory = db.relationship('Memory',
      backref=db.backref('comments'))
  
  message = db.Column(db.BLOB)
  created = db.Column(db.DateTime)

  def __init__(self, user_id, memory_id, message, created=None):
    self.user_id = user_id
    self.memory_id = memory_id
    self.message = message
    if created is None:
      created = datetime.utcnow()
    self.created = created

  def __repr__(self):
    return '<Comment %r : %r>' % (self.user_id, self.message)

  def get_message(self):
    try:
      return self.message.decode('utf-8')
    except Exception as e:
      return self.message.decode('latin-1')