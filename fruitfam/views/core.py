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
  print 'creating image...'
  img = img_data_to_img_object(image_data)
  # Guess components
  print 'guessing components...'
  comps, clarifai_tags = guess_components(img)
  # Create food
  print 'uploading food item...'
  streak, food_item_id = upload_food_item(g.user, img, clarifai_tags, timezone)
  
  print 'serializing image...'
  serialized_image = serialize_image(img)
  set_shareable_photo.delay(food_item_id, serialized_image)
  
  print 'returning comp data...'
  # Get comp
  component = comps[0]
  message = component.get_message()
  
  db.session.commit()
  return jsonify(
    foodItemId=food_item_id,
    isFruit=1,
    title=component.name,
    healthInfo="\xe2\x98\x9d\xf0\x9f\x8f\xbe Potasium, Vitamin A, C \n \xf0\x9f\x98\x81 34cal per cup",
    message=message,
    streak=streak,
    token=g.user.token
  )

@app.route('/upload/shareable_photo', methods=['POST'])
@auth.login_required
def upload_shareable_photo():
  data = request.form
  food_item_id = data['foodItemId']
  image_data = request.files.get('docfile', None)
  
  img = img_data_to_img_object(image_data)
  serialized_image = serialize_image(img)
  set_shareable_photo.delay(food_item_id, serialized_image)
  
  return 200, 'cool'

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

@app.route('/load/diary', methods=['GET', 'POST'])
@auth.login_required
def load_diary():
  requesting_user = g.user
  diary_user_id = request.json('user_id', requesting_user.id)
  diary_user = User.query.filter_by(id=diary_user_id).one()
  diary = get_diary(diary_user, requesting_user)
  return jsonify(
    playerName=diary_user.name(),
    profilePhotoUrl=diary_user.get_profile_photo(),
    missionDescription="Eat 2 red fruits in a 24 hour period \xf0\x9f\x8d\x92\xf0\x9f\x8d\x93",
    playerLevel=diary_user.get_level(),
    recipeCount=52,
    bootyNumerator=240,
    bootyDenominator=400,
    maxStreak=diary_user.get_max_streak(),
    totalPhotos=len(diary),
    photos=diary
  )


@app.route('/load/feed', methods=['GET', 'POST'])
@auth.login_required
def load_feed():
  requesting_user = g.user
  
  comment_object = {
    'message' : "whoa that looks amazing",
    'playerName' : "Abhinav Vadrevu",
    'playerProfileUrl' : 'https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-1/c349.149.312.312/s160x160/11161343_10153393544189095_5097894419925828650_n.jpg?oh=c0d181176fb41051a0022ae20ba9034c&oe=5946493C'
  }
  
  card = {
    'fullscreenUrl': "https://s3.amazonaws.com/fruitfam/a5yqtLZLi225dnt9O2EvzJph5UIB3W0kHWnkMJqEgxyBSzTlvI",
    'playerName' : "Abhinav Vadrevu",
    'playerLevel' : 6,
    'photoTimeDescription' : "Saturday 9:13am",
    'profilePhotoUrl' : "https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-1/c349.149.312.312/s160x160/11161343_10153393544189095_5097894419925828650_n.jpg?oh=c0d181176fb41051a0022ae20ba9034c&oe=5946493C",
    'likesCount' : 235,
    'likedByRequester': 1, # 1 or 0 if this user liked this already,
    'comments': [comment_object]*3,
    'playerId': 235 # userId of user that created this photo
  }
  
  return jsonify(
    feed=[card]*10
  )
  