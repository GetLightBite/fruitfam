from datetime import datetime
from fruitfam import db

class FoodItem(db.Model):
  __tablename__ = 'food_items'
  id = db.Column(db.Integer, primary_key = True)
  
  clarifai_tags = db.Column(db.BLOB)
  client_timestamp = db.Column(db.Integer)
  num_likes = db.Column(db.Integer, default=0)
  not_food = db.Column(db.Boolean, default = False)
  created = db.Column(db.DateTime)
  
  # Generated data
  img_url_icon = db.Column(db.String(255), index = True) # 100x100
  img_url_diary = db.Column(db.String(255), index = True) # 414x587
  img_url_fullscreen = db.Column(db.String(255), index = True) # 720x?
  img_url_original = db.Column(db.String(255), index = True) # 1500x?
  img_url_recognition = db.Column(db.String(255), index = True) # 512x?
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', backref=db.backref('food_items'))

  def __init__(self, user, created=None):
    self.user = user
    if created is None:
      created = datetime.utcnow()
    self.created = created
  
  def img_url_recognition(self):
    if self.img_url_recognition != None:
      return img_url_recognition
    return ''
  
  def img_url_fullscreen(self):
    if self.img_url_fullscreen != None:
      return img_url_fullscreen
    return self.img_url_recognition()

  def __repr__(self):
    return '<FoodItem %r>' % self.id
