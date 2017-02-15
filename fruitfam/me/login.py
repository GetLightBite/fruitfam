import facebook
from fruitfam import db
from fruitfam.models.component import Component
from fruitfam.models.user import User
from fruitfam.models.user_mission import UserMission
from fruitfam.tasks.fb_login import fb_login
from sqlalchemy import func

def login_user(fb_token):
  # Get fb ID:
  print '1.1'
  graph = facebook.GraphAPI(fb_token)
  print '1.2'
  args = {'fields' : 'id' }
  user_fb_id = None
  print '1.3'
  try:
    print '1.4'
    profile_data = graph.get_object('me', **args)
    print '1.5'
    user_fb_id = profile_data.get('id', None)
    print '1.6'
  except Exception as e:
    pass
  if user_fb_id != None:
    existing_user = User.query.filter_by(fb_id=user_fb_id).first()
    if existing_user != None:
      if fb_token != existing_user.fb_token:
        existing_user.fb_token = fb_token
        db.session.add(existing_user)
        db.session.commit()
      return existing_user, 0
  
  random_fruit_name = Component.query.order_by(func.rand()).first().name
  new_user, token = User.create_user('Anonymous',
    random_fruit_name, 'someemail', fb_token=fb_token, fb_id=user_fb_id)
  fb_login.delay(new_user.id)
  
  # Now create the users first mission!
  user_mission = UserMission(new_user, 1)
  db.session.add(user_mission)
  db.session.commit()
  return new_user, 1