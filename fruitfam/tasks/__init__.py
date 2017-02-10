from celery.task.control import discard_all

# Clear the redis queue
print 'Clearing queue'
discard_all()

# Reschedule notifs for all current missions
def reschedule_notifs():
  from fruitfam.models.user_mission import UserMission
  current_user_missions = UserMission.query.filter_by(
    is_over=False
  ).all()
  for mission in current_user_missions:
    rules = mission.get_rules()
    rules.schedule_notifs()

reschedule_notifs()

from fruitfam import celery
from fb_login import *
from level1_reminders import *
from notifications import *
from update_food_item import *
from utils import *