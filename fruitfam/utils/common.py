from datetime import datetime
import facebook
from fruitfam import db
from fruitfam.models.user import User
from fruitfam.models.component import Component
import json
import os
import sendgrid
from sqlalchemy.exc import InvalidRequestError
from PIL import Image

kSendGridApiKey = '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'
sg = sendgrid.SendGridClient(kSendGridApiKey)

def is_prod():
  env = os.environ.get('ENV', 'DEVEL')
  return env == 'PROD'

def send_email(to_email, sbj, msg_html, fullname = None, bcc_email=None):
  if is_prod():
    message = sendgrid.Mail()
    if bcc_email != None:
      message.add_bcc(bcc_email)
    message.add_to(to_email)
    message.set_from("founders@kalekam.com")
    message.set_subject(sbj)
    message.set_html(msg_html)
    if fullname is not None:
      message.add_to_name(fullname)
    sg.send(message)

def serialize_image(img):
  image = {
    'pixels': img.tobytes(),
    'size': img.size,
    'mode': img.mode,
  }
  return image

def deserialize_image(image):
  img = Image.frombytes(
    image['mode'],
    image['size'],
    image['pixels']
  )
  return img

def send_notification(message, user_id, badge_increment=0, params={}, title=None):
  from fruitfam.tasks.notifications import send_notification as send_notification_celery
  send_notification_celery.delay(message.decode('utf-8'), user_id, badge_increment, params, title.decode('utf-8'))

def date_to_datetime(date):
  return datetime.combine(date, datetime.min.time())

def get_user_friends(user):
  try:
    fb_token = user.fb_token
    graph = facebook.GraphAPI(fb_token)
    args = {'fields' : 'id,name,friends' }
    profile_data = graph.get_object('me', **args)
    friend_data = profile_data['friends']['data']
    fb_ids = []
    for data in friend_data:
      fb_id = data['id']
      fb_ids.append(fb_id)
    users = User.query.filter(User.fb_id.in_(fb_ids)).all()
    return users
  except Exception as e:
    print e
    return []

def food_item_upload_email(food_item, session):
  now = datetime.utcnow()
  user = session.query(User).filter_by(id=food_item.user_id).one()
  user_name = user.real_name()
  component_id = food_item.component_id
  food_name = 'something'
  if component_id != None:
    component = session.query(Component).filter_by(id=component_id).one()
    food_name = component.name
  
  subject = "Fruit log report: %s ate %s" % (user_name, food_name)
  
  msg_html = """<br /><img src="%s" style="width: 400px;"><h3 style="font-family: 'Avenir Next','Helvetica Neue',Arial,Helvetica,sans-serif; font-weight:400; color: black;">""" % food_item.recognition_img()
  
  if food_item.clarifai_tags != None:
    clarifai_tags = json.loads(food_item.clarifai_tags)
    clarifai_guess_text = '<br />'.join(map(lambda x: '%s    %s' % (x[1], x[0]), clarifai_tags[0:5]))
    # component_guesses = clarifai_tags_to_components_list(clarifai_tags)
    # top_five_components = component_guesses[0:5]
    # top_five_component_names = '<br />'.join(map(lambda x: x.name, top_five_components))
    # msg_html += '<b>Component guesses were:</b><br />%s' % str(top_five_component_names)
    msg_html += '<br /><br /><b>Top 5 Clarifai guesses were:</b><br />%s' % clarifai_guess_text
  
  msg_html += '<br /><br />Users local time at upload was: <b>%s</b>' % user.local_time().strftime("%I:%M %p on %a, %d %b")
  
  msg_html += '<br /><br />User ID is %d, food item ID is %d' % (user.id, food_item.id)
  send_email('founders@kalekam.com', subject, msg_html, fullname='Founders')


def send_report_exception_email(exception, g, url, args=None):
  subject = "Exception detected in FruitFam prod app!"
  try:
    user_id, user_name = str(g.user.id), str(g.user.firstname)
  except AttributeError, e:
    user_id, user_name = 'Unknown', 'Unknown'
  except InvalidRequestError, e:
    db.session.rollback()
    user_id, user_name = str(g.user.id), str(g.user.firstname)
  msg_html = '''There was an exception detected:
  <br />
  {0}
  <br />
  User ID causing the exception: {1}
  <br />
  User first name causing the exception: {2}
  <br />
  Url hit: {3}
  <br />
  Args were:
  <br />
  <div style="font-family: Courier New">{4}</div>
  <br />
  Best,
  <br />
  The FruitFam team
  '''.format(str(exception), user_id, user_name, url, json.dumps(args))
  print msg_html
  send_email('founders@kalekam.com', subject, msg_html, fullname='Founders')