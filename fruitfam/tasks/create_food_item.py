from fruitfam import celery, db
from fruitfam.models.user import User
from fruitfam.models.food_item import FoodItem
from fruitfam.tasks.utils import FruitFamTask
from fruitfam.utils.upload_image import upload_image_from_object
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
def create_food_item(user_id, serialized_image, clarifai_tags):
  user = db.session.query(User).filter_by(id=user_id).one()
  food_item = FoodItem(user)
  db.session.add(food_item)
  food_item.clarifai_tags = json.dumps(clarifai_tags)
  
  # upload image to S3
  img = deserialize_image(serialized_image)
  url = upload_image_from_object(img)
  food_item.img_url_recognition = url
  print 'commit over'

