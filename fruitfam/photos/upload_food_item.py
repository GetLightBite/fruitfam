from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.models.food_item import FoodItem
from fruitfam.models.user_mission import UserMission
from fruitfam.tasks.update_food_item import set_food_item_recognition_img
from fruitfam.utils.common import serialize_image
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.upload_image import compress_image, crop_img_to_square, crop_img_to_diary_dims, resize_image, upload_image_from_object
from multiprocessing import Manager, Process
from sqlalchemy.orm import sessionmaker

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

def upload_recognition_image(img, food_item_id):
  manager = Manager()
  upload_image_process = Process(
    target=upload_recognition_image_parallel,
    args=(
      img,
      food_item_id
    )
  )
  upload_image_process.start()

def upload_food_item_image(img, food_item_id):
  manager = Manager()
  upload_image_process = Process(
    target=upload_and_set_image_parallel,
    args=(
      img,
      food_item_id
    )
  )
  upload_image_process.start()

def upload_recognition_image_parallel(img, food_item_id):
  engine = db.engine
  Session = sessionmaker(bind=engine)
  session = Session()
  food_item = session.query(FoodItem).filter_by(id=food_item_id).one()
  # upload image to S3
  url = upload_image_from_object(img)
  food_item.img_url_recognition = url
  session.add(food_item)
  session.commit()

def upload_and_set_image_parallel(img, food_item_id):
  engine = db.engine
  Session = sessionmaker(bind=engine)
  session = Session()
  food_item = session.query(FoodItem).filter_by(id=food_item_id).one()
  # upload image to S3
  original_url = upload_image_from_object(img)
  
  fullscreen_img = resize_image(img, 720)
  fullscreen_url = upload_image_from_object(fullscreen_img)
  
  diary_img = crop_img_to_diary_dims(fullscreen_img)
  diary_img = resize_image(diary_img, 414)
  diary_img_url = upload_image_from_object(diary_img)
  
  icon_square_img = crop_img_to_square(fullscreen_img)
  icon_square_img = resize_image(icon_square_img, 50)
  icon_square_url = upload_image_from_object(icon_square_img)
  
  food_item.img_url_original = original_url
  food_item.img_url_fullscreen = fullscreen_url
  food_item.img_url_diary = diary_img_url
  food_item.img_url_icon = icon_square_url
  session.add(food_item)
  session.commit()