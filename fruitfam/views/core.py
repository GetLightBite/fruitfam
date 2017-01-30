from flask import g, jsonify, request
from fruitfam import app, auth
from fruitfam.models.user import User
from fruitfam.photos.recognize_photo import guess_components

@auth.verify_password
def verify_password(token, password):
  # first try to authenticate by token
  user = User.verify_auth_token(token)
  if not user:
    # return False
    g.user = User.create_user('someuser', 'someuser', 'someemail')
  g.user = user
  return True

@app.route('/')
@auth.login_required
def index():
  return 'Hello World!'

@app.route('/analyze/photo')
@auth.login_required
def analyze_photo():
  user = g.user
  data = request.form
  client_timestamp = data.get('created', None)
  client_timestamp = int(client_timestamp)
  client_meal_id = data.get('randomizedId', None)
  
  image_data = request.files['docfile']
  comps = guess_components(image_data)
  
  return jsonify(
    isFruit = 1,
    title = comps[0].name,
    healthInfo = "\xe2\x98\x9d\xf0\x9f\x8f\xbe Potasium, Vitamin A, C \n \xf0\x9f\x98\x81 34cal per cup",
    message = "Way to go! Enjoy extra energy throughout the day from the rich antioxidants!",
    streak = 7
  )