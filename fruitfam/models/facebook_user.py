from datetime import datetime
from fruitfam import db

class FacebookUser(db.Model):
  __tablename__ = 'facebook_users'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
    backref=db.backref('likes'))
  fb_user_id = db.Column(db.Integer)
  is_family = db.Column(db.Boolean, default = False)
  created = db.Column(db.DateTime)

  # def __init__(self, user_id, food_item_id, created=None):
  #   self.user_id = user_id
  #   self.food_item_id = food_item_id
  #   if created is None:
  #     created = datetime.utcnow()
  #   self.created = created

  # def __repr__(self):
  #   return '<Like %r : %r>' % (self.user_id, self.food_item_id)