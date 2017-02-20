import facebook
from fruitfam import celery, db
from fruitfam.models.user import User
from fruitfam.models.request_log import RequestLog
from fruitfam.tasks.utils import FruitFamTask
from fruitfam.utils.upload_image import upload_image

@celery.task(base=FruitFamTask)
def log_request(url, user_id, ip, env, ms_taken):
  user = db.session.query(User).filter_by(id=user_id).one()
  log = RequestLog(url, user, ip, env, ms_taken)
  db.session.add(log)
  db.session.commit()