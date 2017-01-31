from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.models.food_item import FoodItem
from fruitfam.tasks.create_food_item import create_food_item
from fruitfam.utils.common import serialize_image

def upload_food_item(user, img, clarifai_tags):
  # TODO: offload updating image url data to celery
  # serialized_image = serialize_image(img)
  # create_food_item.delay(user.id, serialized_image, clarifai_tags)
  
  cur_streak = user.streak
  last_upload = user.get_last_log_local()
  curtime = datetime.utcnow()
  last_upload_date = last_upload.date()
  curdate = curtime.date()
  if curtime - last_upload == timedelta(days=1):
    cur_streak += 1
    user.streak = cur_streak
  elif curtime - last_upload > timedelta(days=1):
    user.streak = 1
    cur_streak = 1
  if cur_streak > user.max_streak:
    user.max_streak = cur_streak
  user.last_log = curtime
  db.session.add(user)
  return cur_streak