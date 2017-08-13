from datetime import datetime
# import facebook
from taco import db
from taco.models.user import User
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
  from taco.tasks.notifications import send_notification as send_notification_celery
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

def send_report_exception_email(exception, g, url, args=None):
  subject = "Exception detected in Taco prod app!"
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
  The Taco team
  '''.format(str(exception), user_id, user_name, url, json.dumps(args))
  print msg_html
  send_email('founders@kalekam.com', subject, msg_html, fullname='Founders')