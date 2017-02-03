from datetime import datetime
from fruitfam import db

class Like(db.Model):
  __tablename__ = 'likes'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
    backref=db.backref('likes', lazy='dynamic'))
  food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
  food_item = db.relationship('FoodItem',
      backref=db.backref('likes', lazy='dynamic'))
  created = db.Column(db.DateTime)

  def __init__(self, user_id, food_item_id, created=None):
    self.user_id = user_id
    self.food_item_id = food_item_id
    if created is None:
      created = datetime.utcnow()
    self.created = created

  def __repr__(self):
    return '<Like %r : %r>' % (self.user_id, self.food_item_id)