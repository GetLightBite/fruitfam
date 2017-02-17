from datetime import datetime
from flask import g, jsonify, request, send_from_directory
from fruitfam import app, auth, db
from fruitfam.me.feed import get_feed_cards, get_single_food
from fruitfam.me.actions import like_food_item, unlike_food_item, add_comment
from fruitfam.me.diary import get_diary
from fruitfam.me.login import login_user
from fruitfam.models.blocked_user import BlockedUser
from fruitfam.models.food_item import FoodItem
from fruitfam.models.request_log import RequestLog
from fruitfam.models.user import User
from fruitfam.models.user_mission import UserMission
from fruitfam.photos.recognize_photo import guess_components, request_to_img_object
from fruitfam.photos.upload_food_item import upload_food_item_image, upload_recognition_image, upload_food_item
from fruitfam.tasks.update_food_item import test_endpoint, set_shareable_photo
from fruitfam.tasks.fb_login import fb_login
from fruitfam.utils.common import is_prod, send_report_exception_email, serialize_image
from fruitfam.utils.emoji import Emoji
import os
import sys
import traceback

@auth.verify_password
def verify_password(token, password):
  # first try to authenticate by token
  user = User.verify_auth_token(token)
  g.user = user
  if not user:
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

# Measure request times
@app.before_request
def before_request():
  g.last_request_start = datetime.utcnow()

@app.after_request
def log_request_stats(r):
  ms_taken = (datetime.utcnow() - g.last_request_start).total_seconds() * 1000
  url = request.url_rule
  if url == None:
    url = 'unknown'
  try:
    user = g.user
  except AttributeError, e:
    user = None
  ip = request.remote_addr
  env = os.environ.get('ENV', 'DEVEL')
  utctime = datetime.utcnow()
  log = RequestLog(url, user, ip, env, ms_taken)
  db.session.add(log)
  db.session.commit()
  r.cache_control.max_age = 1209600
  return r

# Handle exceptions in prod
if is_prod():
  @app.errorhandler(Exception)
  def all_exception_handler(error):
    print 'Reporting an exception!'
    args1 = dict(request.args) if request.args != None else {}
    args2 = dict(request.json) if request.json != None else {}
    args3 = dict(request.form) if request.form != None else {}
    args = args1
    args.update(args2)
    args.update(args3)
    etype, value, tb = sys.exc_info()
    traceback_lst = traceback.format_exception(etype, value, tb)
    traceback_str = '<br />'.join(map(lambda x: x.strip(), traceback_lst))
    error_message = error.message
    url = request.url_rule
    exception_str = '<div style="font-family: Courier New"><h3>%s</h3><p>%s</p></div>' % (error_message, traceback_str)
    send_report_exception_email(exception_str, g, url, args=args)
    raise error

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
  instructions = [
    'Get fit by completing each mission in this game ' + Emoji.running_woman(),
    'Level up by collecting booty points. Earn these by completing missions\n%s%s%s = %s' % (Emoji.peach(), Emoji.peach(), Emoji.peach(), Emoji.trophy()),
    'Beat the first few missions by eating more fruit %s%s. Advanced levels will focus on other parts of your diet %s%s' % (Emoji.watermelon(), Emoji.strawberry(), Emoji.bread(), Emoji.sushi()),
    'First Mission: You have 120 seconds to find a fruit and take a picture of it...  and then eat it!! %s%s' % (Emoji.camera(), Emoji.watermelon())
  ]
  tutorial = {
    'title': 'Welcome to FruitFam %s%s' % (Emoji.peach(), Emoji.family()),
    'messages' : instructions
  }
  return jsonify(
    playerId=user.id,
    token=user.token,
    mission=mission,
    isNewUser=is_new_user,
    tutorial=tutorial
  )

@app.route("/upload/apns_token", methods=['POST'])
@auth.login_required
def upload_apns_token():
  apns_token = request.json['token']
  g.user.apns_token = apns_token
  db.session.add(g.user)
  db.session.commit()
  return '', 204

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
  json_resp = upload_food_item(g.user, img, clarifai_tags, comps, timezone, image_type)
  
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
  if g.user.level == 1:
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
  print streak, max_streak
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
  print mission
  diary = get_diary(diary_user, requesting_user)
  return jsonify(
    playerName=diary_user.name(),
    profilePhotoUrl=diary_user.get_profile_photo(),
    playerLevel=diary_user.get_level(),
    recipeCount=0,
    bootyNumerator=user_mission.get_booty(),
    bootyDenominator=rules.target_booty(),
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

@app.route('/delete/food_item', methods=['POST'])
@auth.login_required
def delete_food_item():
  food_item_id = request.json['foodItemId']
  f = FoodItem.query.filter_by(id=food_item_id).one()
  if g.user.id == f.user_id:
    db.session.delete(f)
    db.session.commit()
    return jsonify(
      ok='cool'
    )
  return 'Permission Denied', 550

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

@app.route('/test_exception', methods=['GET'])
def exception_throwing():
  raise Exception('TEST EXCEPTION!')
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