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
  fullscreen_url = upload_image_from_object(img)
  
  large_img = resize_image(img, 720)
  large_url = upload_image_from_object(large_img)
  
  square_img = crop_img_to_square(large_img)
  small_square_img = resize_image(square_img, 150)
  small_square_url = upload_image_from_object(small_square_img)
  
  tiny_square_img = resize_image(square_img, 50)
  tiny_square_url = upload_image_from_object(tiny_square_img)
  
  food_item.img_url_fullscreen = fullscreen_url
  food_item.img_url_large = large_url
  food_item.img_url_small = small_square_url
  food_item.img_url_tiny = tiny_square_url
  db.session.add(food_item)
  db.session.commit()
