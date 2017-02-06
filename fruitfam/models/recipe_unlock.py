from datetime import datetime
from fruitfam import db

class RecipeUnlock(db.Model):
  __tablename__ = 'recipe_unlocks'
  id = db.Column(db.Integer, primary_key = True)
  
  # associated recipe
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
  recipe = db.relationship('Recipe',
    backref=db.backref('recipe_unlocks'))
  
  # associated user
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User',
    backref=db.backref('recipe_unlocks'))
  
  unlock_time = db.Column(db.DateTime)

  def __init__(self, user, recipe, unlock_time=None):
    
    self.user = user
    self.recipe = recipe
    if unlock_time is None:
      unlock_time = datetime.utcnow()
    self.unlock_time = unlock_time
  
  def __repr__(self):
    return '<RecipeUnlock user %r -> recipe %r>' % (self.user_id, self.recipe_id)