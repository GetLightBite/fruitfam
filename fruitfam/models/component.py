from datetime import datetime

from fruitfam import db


class Component(db.Model):
  __tablename__ = "components"
  id = db.Column(db.Integer, primary_key = True)
  
  name = db.Column(db.String(255))
  # category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
  
  health_info = db.Column(db.String(255))
  message = db.Column(db.String(255))
  
  vitamins = db.Column(db.String(255))
  cals = db.Column(db.String(255))
  benefits = db.Column(db.String(255))

  def __init__(self, name):
    self.name = name
  
  def get_health_info(self):
    if self.health_info != None:
      return self.health_info
    return ''
  
  def get_message(self):
    if self.message != None:
      return self.message
    return ''
  
  def __repr__(self):
    return '<Component %s>' % self.name