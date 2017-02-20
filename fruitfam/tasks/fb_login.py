import facebook
from facebook import GraphAPIError
from fruitfam import celery, db
from fruitfam.models.user import User
from fruitfam.tasks.utils import FruitFamTask
from fruitfam.utils.upload_image import upload_image

@celery.task(base=FruitFamTask)
def fb_login(user_id):
  user = db.session.query(User).filter_by(id=user_id).one()
  fb_token = user.fb_token
  # Get user info
  graph = facebook.GraphAPI(fb_token)
  args = {'fields' : 'id,name,email,gender,age_range,first_name,last_name,friends.limit(1000)' }
  try:
    profile_data = graph.get_object('me', **args)
    user_fb_id = profile_data['id']
    picture_data = graph.get_object('%s/picture?type=large' % user_fb_id)
  except GraphAPIError as e:
    pass
  # Set user info
  firstname = profile_data['first_name']
  lastname = profile_data['last_name']
  email = profile_data.get('email', None)
  gender = profile_data.get('gender', None)
  profile_url = picture_data.get('url', None)
  if profile_url != None:
    profile_url = upload_image(profile_url, width=200, is_square=True)
  user.firstname = firstname
  user.lastname = lastname
  user.email = email
  user.gender = gender
  user.profile_photo = profile_url
  db.session.add(user)
  db.session.commit()