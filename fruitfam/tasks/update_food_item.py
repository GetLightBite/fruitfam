from fruitfam import celery, db
from fruitfam.models.user import User
from fruitfam.models.food_item import FoodItem
from fruitfam.tasks.utils import FruitFamTask
from fruitfam.utils.upload_image import crop_img_to_square, resize_image, upload_image_from_object
from fruitfam.utils.common import deserialize_image
import json
import time

@celery.task(base=FruitFamTask)
def test_endpoint(newstreak):
  print 'sleeping 5 seconds'
  time.sleep(5)
  print 'getting user'
  user = db.session.query(User).filter_by(id=1).one()
  user.max_streak = newstreak
  db.session.add(user)
  db.session.commit()
  print 'commit over'

@celery.task(base=FruitFamTask)
def set_food_item_recognition_img(food_item_id, serialized_image, clarifai_tags):
  food_item = db.session.query(FoodItem).filter_by(id=food_item_id).one()
  food_item.clarifai_tags = json.dumps(clarifai_tags)
  
  # upload image to S3
  img = deserialize_image(serialized_image)
  url = upload_image_from_object(img)
  food_item.img_url_recognition = url
  db.session.commit()

@celery.task(base=FruitFamTask)
def set_shareable_photo(food_item_id, serialized_image):
  food_item = db.session.query(FoodItem).filter_by(id=food_item_id).one()
  
  # upload image to S3
  img = deserialize_image(serialized_image)
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
