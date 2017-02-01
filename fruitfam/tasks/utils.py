from celery import Task
from celery.task.control import discard_all
from datetime import datetime
from fruitfam import app, celery, db
from fruitfam.utils.common import send_email
import json
import os
import re
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import func
import time
import traceback

# Clear the redis queue
print 'Clearing queue'
discard_all()

class FruitFamTask(Task):
  """
  Reports issues and closes sessions. Does administrative work with tasks
  """
  abstract = True
  def on_failure(self, exc, task_id, args, kwargs, einfo):
    self.email_exception(exc, task_id, args, kwargs, einfo)
    db.session.remove()
    super(FruitFamTask, self).on_failure(exc, task_id, args, kwargs, einfo)
  
  def email_exception(self, exc, task_id, args, kwargs, einfo):
    error_traceback = '<br />'.join(
      traceback.format_exception(einfo.type, einfo.exception, einfo.tb),
    )
    url = 'Celery Task ID %s' % task_id
    exception_str = '<div style="font-family: Courier New"><h3>%s</h3><p>%s</p></div>' % (exc, error_traceback)
    subject = "Exception detected in Celery prod app!"
    jargs = ''
    try:
      jargs = json.dumps(args)
    except Exception as e:
      pass
    msg_html = '''There was an exception detected:
    <br /> {0}
    <br /> User ID causing the exception: {1}
    <br /> User first name causing the exception: {2}
    <br /> Url hit: {3}
    <br /> Args were:
    <br /> <div style="font-family: Courier New">{4}</div>
    <br /> Best,
    <br /> The KaleKam team
    '''.format(str(exception_str), 'Celery', 'Celery Dude', url, jargs)
    print 'Errors in devel not reported'
    send_email('abhinav@kalekam.com', subject, msg_html, fullname = None, bcc_email=None)
  
  def after_return(self, status, retval, task_id, args, kwargs, einfo):
    db.session.remove()

def get_session():
  engine = db.engine
  Session = sessionmaker(bind=engine)
  session = Session()
  session.close()
  return session

def close_session(session):
  session.bind.dispose()
  session.close()