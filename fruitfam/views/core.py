from flask import g, jsonify, request
from fruitfam import app, auth, db
from fruitfam.models.user import User
from fruitfam.models.food_item import FoodItem
from fruitfam.photos.recognize_photo import guess_components, img_data_to_img_object
from fruitfam.photos.upload_food_item import upload_food_item
from fruitfam.tasks.update_food_item import test_endpoint, set_shareable_photo
from fruitfam.utils.common import serialize_image

@auth.verify_password
def verify_password(token, password):
  # first try to authenticate by token
  user = User.verify_auth_token(token)
  g.user = user
  if not user:
    # return False
    g.user, token = User.create_user('someuser', 'someuser', 'someemail')
  return True

@app.route('/')
@auth.login_required
def index():
  test_endpoint.delay(4)
  return 'Hello World!'

@app.route('/analyze/photo', methods=['POST'])
@auth.login_required
def analyze_photo():
  user = g.user
  data = request.form
  timezone = data.get('timezone', -8)
  client_timestamp = data.get('created', -1)
  client_timestamp = int(client_timestamp)
  client_meal_id = data.get('randomizedId', None)
  image_data = request.files.get('docfile', None)
  
  # Create image
  img = img_data_to_img_object(image_data)
  # Guess components
  comps, clarifai_tags = guess_components(img)
  # Create food
  streak, food_item_id = upload_food_item(g.user, img, clarifai_tags, timezone)
  
  serialized_image = serialize_image(img)
  set_shareable_photo.delay(food_item_id, serialized_image)
  
  db.session.commit()
  return jsonify(
    foodItemId=food_item_id,
    isFruit=1,
    title=comps[0].name,
    healthInfo="\xe2\x98\x9d\xf0\x9f\x8f\xbe Potasium, Vitamin A, C \n \xf0\x9f\x98\x81 34cal per cup",
    message="Way to go! Enjoy extra energy throughout the day from the rich antioxidants!",
    streak=streak,
    token=g.user.token
  )

@app.route('/upload/shareable_photo', methods=['POST'])
@auth.login_required
def upload_shareable_photo():
  user = g.user
  data = request.form
  food_item_id = data['foodItemId']
  image_data = request.files.get('docfile', None)
  
  img = img_data_to_img_object(image_data)
  serialized_image = serialize_image(img)
  set_shareable_photo.delay(food_item_id, serialized_image)
  
  return jsonify(
    isFruit=1,
    title=comps[0].name,
    healthInfo="\xe2\x98\x9d\xf0\x9f\x8f\xbe Potasium, Vitamin A, C \n \xf0\x9f\x98\x81 34cal per cup",
    message="Way to go! Enjoy extra energy throughout the day from the rich antioxidants!",
    streak=streak,
    token=g.user.token
  )

@app.route('/get_streak', methods=['GET'])
@auth.login_required
def get_streak():
  user = g.user
  streak = user.streak
  max_streak = user.max_streak
  return jsonify(
    current = streak,
    max = max_streak
  )
  