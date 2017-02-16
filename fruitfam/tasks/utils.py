from celery import Task
from datetime import datetime
from fruitfam import app, celery, db
import json
import os
import re
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import func
import time
import traceback

class FruitFamTask(Task):
  """
  Reports issues and closes sessions. Does administrative work with tasks
  """
  abstract = True
  
  # def __init__(self, *args, **kwargs):
  #   print 'args', args
  #   print 'kwargs', kwargs
  #   super(FruitFamTask, self).__init__(*args, **kwargs)
  
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
    <br /> The FruitFam team
    '''.format(str(exception_str), 'Celery', 'Celery Dude', url, jargs)
    print 'Errors in devel not reported'
    from fruitfam.utils.common import send_email
    send_email('abhinav@kalekam.com', subject, msg_html, fullname = None, bcc_email=None)
  
  def after_return(self, status, retval, task_id, args, kwargs, einfo):
    db.session.remove()
  
  # def run(self, *args, **kwargs):
  #   print 'RUN methods'
  #   print 'args:'
  #   print args
  #   print 'kwargs:'
  #   print kwargs
  #   super(FruitFamTask, self).run(*args, **kwargs)
  
  # def delay(self, *args, **kwargs):
  #   print 'DELAY method'
  #   print 'args:'
  #   print args
  #   print 'kwargs:'
  #   print kwargs
  #   super(FruitFamTask, self).delay(*args, **kwargs)
  
  # def apply(self, args=None, kwargs=None,
  #             link=None, link_error=None,
  #             task_id=None, retries=None, throw=None,
  #             logfile=None, loglevel=None, headers=None, **options):
  #   print 'args', args
  #   print 'kwargs', kwargs
  #   print 'link', link
  #   print 'link_error', link_error
  #   print 'task_id', task_id
  #   print 'retries', retries
  #   print 'throw', throw
  #   print 'headers', headers
  #   print 'options', options
  #   super(FruitFamTask, self).apply(args, kwargs, link, link_error, task_id, retries, throw, logfile, loglevel, headers, **options)

def get_session():
  engine = db.engine
  Session = sessionmaker(bind=engine)
  session = Session()
  session.close()
  return session

def close_session(session):
  session.bind.dispose()
  session.close()