from flask import g, jsonify, request, send_from_directory
from fruitfam import app, auth, db
from fruitfam.me.feed import get_feed_cards, get_single_food
from fruitfam.me.actions import like_food_item, unlike_food_item, add_comment
from fruitfam.me.diary import get_diary
from fruitfam.me.login import login_user
from fruitfam.models.blocked_user import BlockedUser
from fruitfam.models.user import User
from fruitfam.models.user_mission import UserMission
from fruitfam.photos.recognize_photo import guess_components, request_to_img_object
from fruitfam.photos.upload_food_item import upload_food_item_image, upload_recognition_image, upload_food_item, upload_food_item2
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
  user, is_new_user = login_user(fb_token)
  g.user = user
  # Get the first mission!
  user_mission = UserMission.query.filter(
    UserMission.user_id == g.user.id
  ).filter(
    UserMission.is_over == False
  ).one()
  rules = user_mission.get_rules()
  mission = rules.get_mission_json()
  return jsonify(
    playerId=user.id,
    token=user.token,
    mission=mission,
    isNewUser=is_new_user
  )

@app.route("/upload/apns_token", methods=['POST'])
@auth.login_required
def upload_apns_token():
  apns_token = request.json['token']
  g.user.apns_token = apns_token
  db.session.add(g.user)
  db.session.commit()
  return '', 204

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
  # image_data = request.files.get('docfile', None)
  
  # Create image
  img = request_to_img_object(request)
  # Guess components
  image_type, comps, clarifai_tags = guess_components(img)
  # Create food
  json_resp = upload_food_item2(g.user, img, clarifai_tags, comps, timezone, image_type)
  
  food_item_id = json_resp['recognition']['foodItemId']
  db.session.commit()
  upload_recognition_image(img, food_item_id)
  print 'resp'
  print json_resp
  return jsonify(**json_resp)

@app.route('/upload/shareable_photo', methods=['POST'])
@auth.login_required
def upload_shareable_photo():
  user = g.user
  data = request.form
  food_item_id = data['foodItemId']
  image_data = request.files.get('docfile', None)
  
  # Create image
  img = request_to_img_object(request)
  upload_food_item_image(img, food_item_id)
  
  return ('', 204)

@app.route('/report/mission_timeout', methods=['POST'])
@auth.login_required
def timout_mission():
  user_mission = UserMission.query.filter(
    UserMission.user_id == g.user.id
  ).filter(
    UserMission.is_over == False
  ).one()
  user_mission.increment_timeouts_reached()
  rules = user_mission.get_rules()
  rules.schedule_notifs() # Schedule a notif to go off at 8pm
  return ('', 204)

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
  diary_user_id = request.args.get('player_id', requesting_user.id)
  diary_user = User.query.filter_by(id=diary_user_id).one()
  user_mission = UserMission.query.filter(
    UserMission.user_id == diary_user_id
  ).filter(
    UserMission.is_over == False
  ).one()
  rules = user_mission.get_rules()
  mission = rules.get_mission_json()
  diary = get_diary(diary_user, requesting_user)
  return jsonify(
    playerName=diary_user.name(),
    profilePhotoUrl=diary_user.get_profile_photo(),
    playerLevel=diary_user.get_level(),
    recipeCount=0,
    bootyNumerator=user_mission.get_booty(),
    bootyDenominator=rules.target_booty(),
    missionDescription=rules.mission_description(),
    maxStreak=diary_user.get_max_streak(),
    totalPhotos=len(diary),
    photos=diary,
    mission=mission
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
  user_id = request.args['userId']
  u = User.query.filter_by(id=user_id).one()
  db.session.delete(u)
  db.session.commit()
  return jsonify(
    ok='cool'
  )

@app.route('/block/player', methods=['POST'])
@auth.login_required
def block_user():
  user_id = request.json['playerId']
  block = BlockedUser(g.user.id, user_id)
  db.session.add(block)
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