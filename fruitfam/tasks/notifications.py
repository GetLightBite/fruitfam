from apns import APNs, Payload
from fruitfam import celery, db
from fruitfam.models.user import User
from fruitfam.tasks.utils import FruitFamTask
# import json
# import time

@celery.task(base=FruitFamTask)
def send_notification(message, user_id, badge_increment, params, title):
  user = db.session.query(User).filter(User.id == user_id).one()
  cert_location = './fruitfam/bin/fruitfam_prod.pem'
  apns = APNs(use_sandbox=False, cert_file=cert_location, key_file=cert_location)
  env = os.environ.get('ENV', 'devel')
  if env == 'prod' or (env == 'devel' and user.is_founder()):
    token_hex = user.apns_token
    if token_hex and user.send_notifications:
      print token_hex
      # Send a notification
      try:
        alert_message = message
        if title != None:
          alert_message = {
            'title' : title,
            'body' : message
          }
        payload = Payload(
          alert=alert_message,
          sound="default",
          badge=badge_increment,
          custom=params
        )
        apns.gateway_server.send_notification(str(token_hex), payload)
        if user.is_founder():
          apns = APNs(use_sandbox=True, cert_file=cert_location, key_file=cert_location)
          apns.gateway_server.send_notification(str(token_hex), payload)
      except Exception, e:
        print "Unable to send notif", e
      return apns