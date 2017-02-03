from datetime import timedelta
from fruitfam import app, auth, db
from fruitfam.models.comment import Comment
from fruitfam.models.user import User
from fruitfam.models.food_item import FoodItem
from sqlalchemy import desc, and_
from sqlalchemy.orm import load_only, Load

def construct_card(food_item, user):
  food_item_time = food_item.created
  user_timezone = user.last_timezone()
  food_item_local_time = food_item_time + timedelta(hours=user_timezone)
  food_item_time_str = food_item_local_time.strftime("%A %-I:%M%p")
  comment_object = {
    'message' : "whoa that looks amazing",
    'playerName' : "Abhinav Vadrevu",
    'profilePhotoUrl' : 'https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-1/c349.149.312.312/s160x160/11161343_10153393544189095_5097894419925828650_n.jpg?oh=c0d181176fb41051a0022ae20ba9034c&oe=5946493C'
  }
  card = {
    'fullscreenUrl': food_item.fullscreen_img(),
    'playerName' : user.name(),
    'playerLevel' : user.get_level(),
    'photoTimeDescription' : food_item_time_str,
    'profilePhotoUrl' : user.get_profile_photo(),
    'likesCount' : 123,
    'likedByRequester': 0, # 1 or 0 if this user liked this already,
    'comments': [comment_object]*3,
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
    Load(User).load_only('id'),
    Load(User).load_only('firstname'),
    Load(User).load_only('lastname'),
    Load(User).load_only('profile_photo'),
    Load(User).load_only('utc_offset'),
    Load(User).load_only('level')
  ).filter(
    FoodItem.img_url_recognition != None
  ).order_by(
    desc(FoodItem.created)
  ).limit(10).all()
  
  cards = []
  for food_item, user in db_data:
    card = construct_card(food_item, user)
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
    Load(User).load_only('id'),
    Load(User).load_only('firstname'),
    Load(User).load_only('lastname'),
    Load(User).load_only('profile_photo'),
    Load(User).load_only('utc_offset'),
    Load(User).load_only('level')
  ).filter(
    FoodItem.id == food_item_id
  ).one()
  card = construct_card(food_item, user)
  return card