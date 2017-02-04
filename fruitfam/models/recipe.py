from datetime import datetime
from fruitfam import db

class Recipe(db.Model):
  __tablename__ = 'recipes'
  id = db.Column(db.Integer, primary_key = True)
  
  # associated component
  component_id = db.Column(db.Integer, db.ForeignKey('components.id'))
  component = db.relationship('Component',
    backref=db.backref('recipes'))
  
  name = db.Column(db.String(255))
  yummly_recipe_id = db.Column(db.String(255))
  yield_amount = db.Column(db.String(127))
  number_of_servings = db.Column(db.String(127))
  img_url = db.Column(db.String(127))
  prep_time_seconds = db.Column(db.Integer)
  ingredient_lines_json = db.Column(db.BLOB)
  calories = db.Column(db.Integer)
  recipe_source_url = db.Column(db.String(255))
  directions_list = db.Column(db.BLOB)
  yummly_query = db.Column(db.String(127))
  
  created = db.Column(db.DateTime)

  def __init__(self, name, component, yummly_recipe_id, yield_amount, number_of_servings, img_url, prep_time_seconds, ingredient_lines_json, calories, recipe_source_url, directions_list, yummly_query, created=None):
    
    self.name = name
    self.yummly_recipe_id = yummly_recipe_id
    self.yield_amount = yield_amount
    self.number_of_servings = number_of_servings
    self.img_url = img_url
    self.prep_time_seconds = prep_time_seconds
    self.ingredient_lines_json = ingredient_lines_json
    self.calories = calories
    self.recipe_source_url = recipe_source_url
    self.directions_list = directions_list
    self.yummly_query = yummly_query
    if created is None:
      created = datetime.utcnow()
    self.created = created

  def __repr__(self):
    return '<Recipe %s>' % self.name