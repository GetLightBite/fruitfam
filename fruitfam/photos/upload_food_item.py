from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.models.food_item import FoodItem
from fruitfam.models.user_mission import UserMission
from fruitfam.tasks.update_food_item import set_food_item_recognition_img
from fruitfam.utils.common import serialize_image
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.upload_image import compress_image, crop_img_to_square, crop_img_to_diary_dims, resize_image, upload_image_from_object
import json
from multiprocessing import Process
from sqlalchemy.orm import scoped_session, sessionmaker

def upload_food_item(user, img, clarifai_tags, components, timezone, image_type='food'):
  # Update user data
  user.utc_offset = timezone
  db.session.add(user)
  
  # Create an empty food_item
  food_item = FoodItem(user)
  food_item.clarifai_tags = json.dumps(clarifai_tags)
  food_item.component_id = components[0].id
  if image_type != 'food':
    food_item.not_food = True
    food_item.component_id = None
  db.session.add(food_item)
  
  # Deal with non food images
  if image_type != 'food':
    db.session.commit() # Add in the food item
    if image_type == 'person':
      json_response = {}
      recognition_json = {
        'title': 'Hello, beautiful!',
        'message':"You look tasty, but we hear humans are pretty high in calories %s. Maybe go for a fruit instead!" % Emoji.wink(),
        'foodItemId': food_item.id,
        'isFruit':0
      }
      json_response['recognition'] = recognition_json
      return json_response
    if image_type == 'not food':
      json_response = {}
      recognition_json = {
        'title': 'Oh, %s!' % Emoji.poo(),
        'message':"We couldn't figure out what fruit that was %s. Try again from a different angle!" % Emoji.sad(),
        'foodItemId': food_item.id,
        'isFruit':0
      }
      json_response['recognition'] = recognition_json
      return json_response
  
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
  cur_streak = user.get_streak()
  last_upload = user.get_last_log_local()
  curtime = datetime.utcnow()
  cur_user_time = user.local_time()
  last_upload_date = last_upload.date()
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
  # if True:
  #   return
  upload_image_process = Process(
    target=upload_recognition_image_parallel,
    args=(
      img,
      food_item_id
    )
  )
  upload_image_process.start()

def upload_recognition_image_parallel(img, food_item_id):
  engine = db.engine
  session_factory = sessionmaker(bind=engine)
  # session = session_factory()
  Session = scoped_session(session_factory)
  session = Session()
  food_item = session.query(FoodItem).filter_by(id=food_item_id).one()
  # upload image to S3
  url = upload_image_from_object(img)
  food_item.img_url_recognition = url
  session.add(food_item)
  session.commit()
  # Email founders about the image
  food_item_upload_email(food_item, session)
  session.close()
  Session.remove()

def upload_food_item_image(img, food_item_id):
  food_item = db.session.query(FoodItem).filter_by(id=food_item_id).one()
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
  db.session.add(food_item)
  db.session.commit()