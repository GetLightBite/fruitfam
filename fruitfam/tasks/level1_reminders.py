from fruitfam import celery, db
from fruitfam.models.user import User
from fruitfam.tasks.utils import FruitFamTask
from fruitfam.utils.common import send_notification
from fruitfam.utils.emoji import Emoji
from sqlalchemy import func

@celery.task(base=FruitFamTask)
def twenty_min_reminder(user_id):
  user = db.session.query(User).filter_by(id=user_id).one()
  num_logs = db.session.query(func.count(FoodItem.id)).filter_by(user_id=user_id).all()[0][0]
  if num_logs == 0:
    # Remind that there's an extension!
    title="We've given you an extension " + Emoji.stopwatch()
    message = "Reminder: It's not all over! You've got till the end of the day to log a fruit. Beat level 1 and treat your body to a fruit! " + Emoji.tangerine()
    send_notification(message, user_id, badge_increment=0, params={}, title=title)

@celery.task(base=FruitFamTask)
def eight_pm_reminder(user_id):
  user = db.session.query(User).filter_by(id=user_id).one()
  num_logs = db.session.query(func.count(FoodItem.id)).filter_by(user_id=user_id).all()[0][0]
  if num_logs == 0:
    # Remind that it' okay to eat at night
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4425165/
    title="Can eating fruit at night make you fat? " + Emoji.thinking()
    message = ("Renowned nutritionist Alan Aragon %s says no! Keep your streak alive by logging tonight " % Emoji.man()) + Emoji.lightning()
    send_notification(message, user_id, badge_increment=0, params={}, title=title)