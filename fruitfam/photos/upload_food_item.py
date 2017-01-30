from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.models.food_item import FoodItem

def upload_food_item(user, image_data):
  # TODO: offload updating image url data to celery
  food_item = FoodItem(g.user)
  db.session.add(food_item)
  
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
  user.last_log = curtime
  db.session.add(user)
  return cur_streak