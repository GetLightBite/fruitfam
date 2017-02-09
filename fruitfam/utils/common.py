from fruitfam.tasks.notifications import send_notification as send_notification_celery
import os
import sendgrid
from PIL import Image

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
  send_notification_celery.delay(message, user_id, badge_increment, params, title)