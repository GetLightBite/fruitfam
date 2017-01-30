from flask import g, jsonify, request
from fruitfam import app, auth, db
from fruitfam.models.user import User
from fruitfam.models.food_item import FoodItem
from fruitfam.photos.recognize_photo import guess_components
from fruitfam.photos.upload_food_item import upload_food_item

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
  
  # Guess components
  comps = guess_components(image_data)
  
  # Create food
  streak = upload_food_item(g.user, image_data)
  
  # Update user data
  g.user.utc_offset = timezone
  db.session.commit()
  
  return jsonify(
    isFruit=1,
    title=comps[0].name,
    healthInfo="\xe2\x98\x9d\xf0\x9f\x8f\xbe Potasium, Vitamin A, C \n \xf0\x9f\x98\x81 34cal per cup",
    message="Way to go! Enjoy extra energy throughout the day from the rich antioxidants!",
    streak=streak,
    token=g.user.token
  )

@app.route('/streak/status', methods=['GET'])
@auth.login_required
def get_streak():
  user = g.user
  streak=user.streak
  return jsonify(
    streak = streak
  )
  