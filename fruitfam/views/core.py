from flask import g, jsonify, request, send_from_directory
from fruitfam import app, auth, db
from fruitfam.me.feed import get_feed_cards, get_single_food
from fruitfam.me.actions import like_food_item, unlike_food_item, add_comment
from fruitfam.me.diary import get_diary
from fruitfam.me.login import login_user
from fruitfam.models.user import User
from fruitfam.photos.recognize_photo import guess_components, img_data_to_img_object
from fruitfam.photos.upload_food_item import upload_food_item, upload_food_item2
from fruitfam.tasks.update_food_item import test_endpoint, set_shareable_photo
from fruitfam.tasks.fb_login import fb_login
from fruitfam.utils.common import serialize_image
import os

@auth.verify_password
def verify_password(token, password):
  # first try to authenticate by token
  user = User.verify_auth_token(token)
  g.user = user
  if not user:
    # g.user, token = User.create_user('someuser', 'someuser', 'someemail')
    return False
  return True

@app.route('/')
@auth.login_required
def index():
  test_endpoint.delay(4)
  return 'Hello World!'

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'bin'),
    'peach.ico', mimetype='image/vnd.microsoft.icon')

##############
# Core Views #
##############

@app.route('/login/fb', methods=['POST'])
def login():
  fb_token = request.json['fbToken']
  user = login_user(fb_token)
  g.user = user
  return jsonify(
    playerId=user.id,
    token=user.token
  )

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

@app.route('/2/analyze/photo', methods=['POST'])
@auth.login_required
def analyze_photo_2():
  user = g.user
  data = request.form
  timezone = data.get('timezone', -8)
  client_timestamp = data.get('created', -1)
  client_timestamp = int(client_timestamp)
  client_meal_id = data.get('randomizedId', None)
  image_data = request.files.get('docfile', None)
  
  # Create image
  img = img_data_to_img_object(image_data)
  # img = None
  # Guess components
  comps, clarifai_tags = guess_components(img)
  # Create food
  json_resp = upload_food_item2(g.user, img, clarifai_tags, comps, timezone)
  
  serialized_image = serialize_image(img)
  food_item_id = json_resp['foodItemId']
  set_shareable_photo.delay(food_item_id, serialized_image)
  
  # # Get comp
  # component = comps[0]
  # message = component.get_message()
  
  db.session.commit()
  return jsonify(**json_resp)

@app.route('report/mission_timeout', methods=['POST'])
@auth.login_required
def timout_mission():
  user_mission = UserMission.query.filter(
    UserMission.user_id == user.id
  ).filter(
    UserMission.is_over == False
  ).one()
  user_mission.increment_timeouts_reached()
  return 'cool'

@app.route('/3/analyze/photo', methods=['POST'])
@auth.login_required
def analyze_photo_3():
  out = {
    'recognition': {
        'currentStreak': 3,
        'maxStreak': 6,
        'fruitName': "Pomegrante Seeds",
        'healthInfo0':"Potasium, Vitamin A, C",
        'healthInfo1':"34cal per cup",
        'healthInfo2':"Great for smooth skin, silky hair",
        'foodItemId': 15234,
        'isFruit':1
    },
    'bootyPrize': {
        'breakdown': [
            {'title': "Mission 1",
             'booty': 120},
            {'title': "New Fruit",
             'booty': 30},
        ],
        'total': 150
    },

    'newMission': { #// OPTIONAL - IF PLAYER LEVELLED UP
      'missionTitle': "Mission 2",
      'missionDescription': "Eat another fruit tomorrow - reach a 2 day streak of eating fruit daily",
      'currentBooty': 0,
      'missionDetails': {
        'missionType': "timeout",
        'timerSeconds': 8182,
        'onExpiry': "Oh no! Looks like you ran out of 'time':( But since it's your second mission, we'll give you a little longer :)"
      }
    },
    'currentMission': {
      'missionTitle': "Mission 1",
      'missionDescription': "You have 120 seconds to log take a picture of a fruit and eat it!",
      'currentBooty': 32,
      'targetBooty': 300,
      'missionDetails': {
        'missionType': "timeout",
        'timerSeconds': 120,
        'onExpiry': "Oh no! Looks like you ran out of time :( But since it's your first mission, we'll give you a little longer :)"
      }
    },
    'animation': {
        'leveledUp': 1,
        'startBootyNumerator': 23,
        'startBootyDenominator': 200,
        'endBootyNumerator': 1,
        'endBootyDenominator': 400,
        'startMissionDescription': "Eat 2 red fruits in a 24 hour period",
        'endMissionDescription': "Reach a 3 day streak",
        'startPlayerLevel': 1,
        'endPlayerLevel': 2,
    }
  }
  return jsonify(** out)

@app.route('/upload/shareable_photo', methods=['POST'])
@auth.login_required
def upload_shareable_photo():
  data = request.form
  food_item_id = data['foodItemId']
  image_data = request.files.get('docfile', None)
  
  img = img_data_to_img_object(image_data)
  serialized_image = serialize_image(img)
  set_shareable_photo.delay(food_item_id, serialized_image)
  return 'cool'

@app.route('/get_streak', methods=['GET'])
@auth.login_required
def get_streak():
  user = g.user
  streak = user.get_streak()
  max_streak = user.get_max_streak()
  return jsonify(
    current = streak,
    max = max_streak
  )

@app.route('/load/diary', methods=['GET'])
@auth.login_required
def load_diary():
  requesting_user = g.user
  diary_user_id = request.args.get('user_id', requesting_user.id)
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

@app.route('/load/feed', methods=['GET'])
@auth.login_required
def load_feed():
  requesting_user = g.user
  return jsonify(
    feed=get_feed_cards(requesting_user)
  )

@app.route('/like', methods=['POST'])
@auth.login_required
def like():
  requesting_user = g.user
  food_item_id = request.json['foodItemId']
  is_unlike = request.json['isUnlike']
  if is_unlike:
    unlike_food_item(requesting_user.id, food_item_id)
  else:
    like_food_item(requesting_user.id, food_item_id)
  return 'cool'

@app.route('/load/food', methods=['GET'])
@auth.login_required
def load_food():
  requesting_user = g.user
  food_item_id = request.args['foodItemId']
  food_card = get_single_food(requesting_user, food_item_id)
  return jsonify(
    card=food_card
  )

@app.route('/delete/user', methods=['GET'])
def delete_user():
  user_id = request.args['foodItemId']
  u = User.query.filter_by(id=user_id).one()
  db.session.delete(u)
  db.session.commit()
  return jsonify(
    ok='cool'
  )

@app.route('/comment', methods=['POST'])
@auth.login_required
def comment():
  commenting_user = g.user
  food_item_id = request.json['foodItemId']
  message = request.json['message']
  add_comment(commenting_user.id, food_item_id, message)
  return 'cool'