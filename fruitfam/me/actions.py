from fruitfam import db
from fruitfam.models.comment import Comment
# from fruitfam.models.food_item import FoodItem
from fruitfam.models.like import Like
from fruitfam.models.recipe import Recipe
from fruitfam.models.recipe_unlock import RecipeUnlock
from fruitfam.utils.common import send_notification
from fruitfam.utils.emoji import Emoji
# from fruitfam.models.user import User
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

def like_food_item(user_id, food_item_id):
  from fruitfam.tasks.likes import like_notification
  try:
    l = Like(user_id, food_item_id)
    db.session.add(l)
    db.session.commit()
    like_notification.delay(user_id, food_item_id)
  except IntegrityError as e:
    db.session.rollback()
    print 'Attempted to like twice!'

def unlike_food_item(user_id, food_item_id):
  l = Like.query.filter_by(
    user_id=user_id
  ).filter_by(
    food_item_id=food_item_id
  ).first()
  if l != None:
    db.session.delete(l)
    db.session.commit()

def add_comment(user_id, food_item_id, message):
  c = Comment(user_id, food_item_id, message)
  db.session.add(c)
  # TODO: send notification(s)
  db.session.commit()

# def unlock_recipe(user):
#   engine = session.bind
#   sql = text(sql)
#   result = engine.execute(sql)
  
#   recipe_to_unlock = Recipe.query.filter(
    
#   )