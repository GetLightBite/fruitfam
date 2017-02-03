from datetime import datetime
from fruitfam import db

class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
    backref=db.backref('comments'))
  food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
  food_item = db.relationship('FoodItem',
      backref=db.backref('comments'))
  message = db.Column(db.BLOB)
  created = db.Column(db.DateTime)

  def __init__(self, user_id, food_item_id, message, created=None):
    self.user_id = user_id
    self.food_item_id = food_item_id
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