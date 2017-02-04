import facebook
from fruitfam.models.component import Component
from fruitfam.models.user import User
from fruitfam.tasks.fb_login import fb_login

def login_user(fb_token):
  # Get fb ID:
  graph = facebook.GraphAPI(fb_token)
  args = {'fields' : 'id' }
  profile_data = graph.get_object('me', **args)
  user_fb_id = profile_data['id']
  existing_user = User.query.filter_by(fb_id=user_fb_id).first()
  if existing_user != None:
    return existing_user
  
  random_fruit_name = Component.query.order_by(func.rand()).first().name
  new_user, token = User.create_user('Anonymous',
    random_fruit_name, 'someemail', fb_token=fb_token)
  fb_login.delay(new_user.id)
  return new_user