from datetime import timedelta
from fruitfam import app, auth, db
from fruitfam.models.comment import Comment
from fruitfam.models.user import User
from fruitfam.models.food_item import FoodItem
from sqlalchemy import desc, and_
from sqlalchemy.orm import joinedload, load_only, Load

def construct_comment_card(comment, user):
  return {
    'message' : comment.get_message(),
    'playerName' : user.real_name(),
    'profilePhotoUrl' : user.get_profile_photo()
  }

def construct_card(food_item, user, comments):
  food_item_time = food_item.created
  user_timezone = user.last_timezone()
  food_item_local_time = food_item_time + timedelta(hours=user_timezone)
  food_item_time_str = food_item_local_time.strftime("%A %-I:%M%p")
  comment_cards = []
  for comment in comments:
    comment_user = comment.user
    comment_card = construct_comment_card(comment, comment_user)
    comment_cards.append(comment_card)
  card = {
    'foodItemId': food_item.id,
    'fullscreenUrl': food_item.fullscreen_img(),
    'playerName' : user.name(),
    'playerLevel' : user.get_level(),
    'photoTimeDescription' : food_item_time_str,
    'profilePhotoUrl' : user.get_profile_photo(),
    'likesCount' : 123,
    'likedByRequester': 0, # 1 or 0 if this user liked this already,
    'comments': comment_cards,
    'playerId': user.id # userId of user that created this photo
  }
  return card

def get_feed_cards(user):
  db_data = db.session.query(FoodItem, User).join(
    User
  ).options(
    Load(FoodItem).load_only('id'),
    Load(FoodItem).load_only('img_url_diary'),
    Load(FoodItem).load_only('img_url_recognition'),
    Load(FoodItem).load_only('img_url_fullscreen'),
    Load(FoodItem).load_only('created'),
    Load(User).load_only('id'),
    Load(User).load_only('firstname'),
    Load(User).load_only('lastname'),
    Load(User).load_only('profile_photo'),
    Load(User).load_only('utc_offset'),
    Load(User).load_only('level')
  ).options(
    joinedload(FoodItem.comments).load_only('message')
  ).options(
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('id'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('firstname'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('lastname'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('profile_photo'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('utc_offset'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('level'),
  ).filter(
    FoodItem.img_url_recognition != None
  ).order_by(
    desc(FoodItem.created)
  ).limit(50).all()
  
  cards = []
  for food_item, user in db_data:
    comments = food_item.comments
    card = construct_card(food_item, user, comments)
    cards.append(card)
  return cards

def get_single_food(food_item_id):
  food_item, user = db.session.query(FoodItem, User).join(
    User
  ).options(
    Load(FoodItem).load_only('id'),
    Load(FoodItem).load_only('img_url_diary'),
    Load(FoodItem).load_only('img_url_recognition'),
    Load(FoodItem).load_only('img_url_fullscreen'),
    Load(FoodItem).load_only('created'),
    Load(User).load_only('id'),
    Load(User).load_only('firstname'),
    Load(User).load_only('lastname'),
    Load(User).load_only('profile_photo'),
    Load(User).load_only('utc_offset'),
    Load(User).load_only('level')
  ).options(
    joinedload(FoodItem.comments).load_only('message')
  ).options(
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('id'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('firstname'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('lastname'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('profile_photo'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('utc_offset'),
    joinedload(FoodItem.comments).joinedload(Comment.user).load_only('level'),
  ).filter(
    FoodItem.id == food_item_id
  ).one()
  card = construct_card(food_item, user, food_item.comments)
  return card