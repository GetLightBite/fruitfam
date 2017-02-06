from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.models.food_item import FoodItem
from fruitfam.tasks.update_food_item import set_food_item_recognition_img
from fruitfam.utils.common import serialize_image

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
  serialized_image = serialize_image(img)
  print 'serialized image...'
  set_food_item_recognition_img.delay(food_item.id, serialized_image, clarifai_tags)
  print 'upload offloaded to celery'
  
  return cur_streak, food_item.id