from datetime import timedelta
from fruitfam import app, auth, db
from fruitfam.models.blocked_user import BlockedUser
from fruitfam.models.comment import Comment
from fruitfam.models.like import Like
from fruitfam.models.user import User
from fruitfam.models.food_item import FoodItem
from sqlalchemy import desc, and_, not_
from sqlalchemy.orm import joinedload, load_only, Load

def construct_comment_card(comment, user):
  return {
    'message' : comment.get_message(),
    'playerName' : user.real_name(),
    'playerId' : user.id,
    'profilePhotoUrl' : user.get_profile_photo()
  }

def construct_card(requester, food_item, user, comments, likers):
  food_item_time = food_item.created
  user_timezone = user.last_timezone()
  food_item_local_time = food_item_time + timedelta(hours=user_timezone)
  food_item_time_str = food_item_local_time.strftime("%A %-I:%M%p")
  like_user_names = [x.real_name() for x in likers]
  like_user_ids = [x.id for x in likers]
  liked_by_requester = int(requester.id in like_user_ids)
  comment_cards = []
  for comment in comments:
    comment_user = comment.user
    comment_card = construct_comment_card(comment, comment_user)
    comment_cards.append(comment_card)
  comment_cards.reverse()
  card = {
    'foodItemId': food_item.id,
    'fullscreenUrl': food_item.fullscreen_img(),
    'playerName' : user.name(),
    'playerLevel' : user.get_level(),
    'photoTimeDescription' : food_item_time_str,
    'profilePhotoUrl' : user.get_profile_photo(),
    'likesCount' : len(likers),
    'likers' : like_user_names,
    'likedByRequester': liked_by_requester, # 1 or 0 if this user liked this already,
    'comments': comment_cards,
    'playerId': user.id # userId of user that created this photo
  }
  return card

def get_feed_cards(requester):
  db_data = db.session.query(FoodItem).options(
    load_only('id', 'img_url_diary',
      'img_url_recognition', 'img_url_fullscreen', 'created')
  ).options(
    joinedload(FoodItem.user).load_only( 'id', 'firstname',
      'lastname', 'profile_photo', 'utc_offset', 'level')
  ).options(
    joinedload(FoodItem.comments).load_only('message')
  ).options(
    joinedload(FoodItem.comments).joinedload(
      Comment.user
    )#.load_only('firstname', 'lastname', 'profile_photo')
  ).options(
    joinedload(FoodItem.likes).joinedload(
      Like.user
    )#.load_only('id', 'firstname', 'lastname')
  ).filter(
    not_(and_(
      FoodItem.img_url_recognition == None,
      FoodItem.img_url_fullscreen == None
    ))
  ).filter(
    FoodItem.not_food == False
  ).filter(
    not_(
      db.session.query(BlockedUser)
        .filter(FoodItem.user_id == BlockedUser.blocked_user_id)
        .filter(requester.id == BlockedUser.blocking_user_id)
        .exists()
    )
  ).order_by(
    desc(FoodItem.created)
  ).limit(50).all()
  cards = []
  for food_item in db_data:
    user = food_item.user
    comments = food_item.comments
    likes = food_item.likes
    likers = [x.user for x in likes]
    card = construct_card(requester, food_item, user, comments, likers)
    cards.append(card)
  return cards

def get_single_food(requester, food_item_id):
  food_item = db.session.query(FoodItem).options(
    load_only('id', 'img_url_diary',
      'img_url_recognition', 'img_url_fullscreen', 'created')
  ).options(
    joinedload(FoodItem.user).load_only( 'id', 'firstname',
      'lastname', 'profile_photo', 'utc_offset', 'level')
  ).options(
    joinedload(FoodItem.comments).load_only('message')
  ).options(
    joinedload(FoodItem.comments).joinedload(
      Comment.user
    )#.load_only('firstname', 'lastname', 'profile_photo')
  ).options(
    joinedload(FoodItem.likes).joinedload(
      Like.user
    )#.load_only('id', 'firstname', 'lastname')
  ).filter(
    FoodItem.id == food_item_id
  ).one()
  user = food_item.user
  likes = food_item.likes
  likers = [x.user for x in likes]
  card = construct_card(requester, food_item, user, food_item.comments, likers)
  return card