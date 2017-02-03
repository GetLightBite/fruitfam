from fruitfam import db
from fruitfam.models.comment import Comment
# from fruitfam.models.food_item import FoodItem
from fruitfam.models.like import Like
# from fruitfam.models.user import User
from sqlalchemy.exc import IntegrityError

def like_food_item(user_id, food_item_id):
  try:
    l = Like(user_id, food_item_id)
    db.session.add(l)
    db.session.commit()
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