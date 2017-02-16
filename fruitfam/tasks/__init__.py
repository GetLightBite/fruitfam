from fruitfam.tasks.level1_reminders import twenty_min_reminder, eight_pm_reminder
from fruitfam.tasks.simple_pokedex_reminders import simple_pokedex_reminder
from fruitfam.tasks.likes import like_notification
from fruitfam.tasks.notifications import *
from fruitfam.tasks.update_food_item import *

from celery.task.control import discard_all
discard_all()
# # Clear the redis queue
# print 'Clearing queue'

# Reschedule notifs for all current missions
def reschedule_notifs():
  from fruitfam.models.user_mission import UserMission
  current_user_missions = UserMission.query.filter_by(
    is_over=False
  ).all()
  for mission in current_user_missions:
    rules = mission.get_rules()
    rules.schedule_notifs()

# reschedule_notifs()

from fruitfam import celery