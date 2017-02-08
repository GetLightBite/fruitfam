from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.models.food_item import FoodItem
from fruitfam.models.user_mission import UserMission
from fruitfam.tasks.update_food_item import set_food_item_recognition_img
from fruitfam.utils.common import serialize_image
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.upload_image import compress_image

def upload_food_item(user, img, clarifai_tags, timezone):
  # Update user data
  user.utc_offset = timezone
  
  # Create an empty food_item
  food_item = FoodItem(user)
  db.session.add(food_item)
  
  # Update the streak
  cur_streak = user.streak
  last_upload = user.get_last_log_local()
  curtime = datetime.utcnow()
  cur_user_time = user.local_time()
  last_upload_date = last_upload.date()
  curdate = curtime.date()
  cur_user_date = cur_user_time.date()
  if cur_user_date - last_upload_date == timedelta(days=1):
    cur_streak += 1
    user.streak = cur_streak
  elif cur_user_date - last_upload_date > timedelta(days=1):
    user.streak = 1
    cur_streak = 1
  if cur_streak > user.max_streak:
    user.max_streak = cur_streak
  user.last_log = curtime
  db.session.add(user)
  
  # Commit here to get the food_item id
  print 'committing to get food item id...'
  db.session.commit()
  
  # Offload updating image url data to celery
  print 'offloading image upload to celery...'
  compressed_image = compress_image(img)
  serialized_image = serialize_image(compressed_image)
  print 'serialized image...'
  set_food_item_recognition_img.delay(food_item.id, serialized_image, clarifai_tags)
  print 'upload offloaded to celery'
  
  return cur_streak, food_item.id

def upload_food_item2(user, img, clarifai_tags, components, timezone):
  # Update user data
  user.utc_offset = timezone
  
  # Create an empty food_item
  food_item = FoodItem(user)
  db.session.add(food_item)
  
  # Get the right UserMission and get the appropriate json response.
  # Also, call the callback
  user_mission = UserMission.query.filter(
    UserMission.user_id == user.id
  ).filter(
    UserMission.is_over == False
  ).one()
  rules = user_mission.get_rules()
  json_response = rules.log_food(food_item)
  
  # Update the streak
  cur_streak = user.streak
  last_upload = user.get_last_log_local()
  curtime = datetime.utcnow()
  cur_user_time = user.local_time()
  last_upload_date = last_upload.date()
  curdate = curtime.date()
  cur_user_date = cur_user_time.date()
  if cur_user_date - last_upload_date == timedelta(days=1):
    cur_streak += 1
    user.streak = cur_streak
  elif cur_user_date - last_upload_date > timedelta(days=1):
    user.streak = 1
    cur_streak = 1
  if cur_streak > user.max_streak:
    user.max_streak = cur_streak
  user.last_log = curtime
  db.session.add(user)
  
  # Commit here to get the food_item id
  db.session.commit()
  
  # Offload updating image url data to celery
  # compressed_image = compress_image(img)
  # serialized_image = serialize_image(compressed_image)
  # print 'serialized image...'
  # set_food_item_recognition_img.delay(food_item.id, serialized_image, clarifai_tags)
  # print 'upload offloaded to celery'
  recognition_json = {
    'currentStreak': user.streak,
    'maxStreak': user.max_streak,
    'fruitName': components[0].name,
    'healthInfo0':"%s Potasium, Vitamin A, C" % Emoji.point_up(),
    'healthInfo1':"%s 34cal per cup" % Emoji.grinning(),
    'healthInfo2':"%s Great for smooth skin, silky hair" % Emoji.silhouette(),
    'foodItemId': food_item.id,
    'isFruit':1
  }
  json_response['recognition'] = recognition_json
  
  return json_response