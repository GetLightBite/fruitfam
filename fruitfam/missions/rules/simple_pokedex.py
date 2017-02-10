from datetime import datetime, timedelta
from fruitfam.missions.rules.pokedex_mission import PokedexMission
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.common import date_to_datetime

class SimplePokedex(PokedexMission):
  """Log all the fruits in the pokedex!"""
  def __init__(self, user_mission):
    super(Level1, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Collect all the fruits!' + Emoji.lightning()
  
  def rules_text(self):
    return [
      'Eat each of these fruits to complete the mission!' + Emoji.hourglass()
    ]
  
  def mission_id(self):
    return 4
  
  
  
  def booty_call(self):
    return 1
  
  def schedule_notifs(self):
    from fruitfam.tasks.level1_reminders import twenty_min_reminder, eight_pm_reminder
    user_mission = self.get_user_mission()
    user_id = user_mission.user_id
    mission_start = user_mission.created
    now = datetime.utcnow()
    
    # First notif is 20 mins after log to remind user there's an extension
    twenty_mins_after_mission = mission_start + timedelta(minutes=20)
    if twenty_mins_after_mission > now:
      twenty_min_reminder.apply_async(args=[user_id], eta=twenty_mins_after_mission)
    
    # Schedule notif about 4 hours before timeout if possible
    seconds_to_timeout = self.timeout()
    print seconds_to_timeout
    if seconds_to_timeout > 4*60*60+40:
      seconds_to_eight_pm = seconds_to_timeout - 4*60*60
      eight_pm_local = now + timedelta(seconds=seconds_to_eight_pm)
      eight_pm_reminder.apply_async(args=[user_id], eta=eight_pm_local)
    elif seconds_to_timeout > 2*60*60:
      seconds_to_ten_pm = seconds_to_timeout - 2*60*60
      ten_pm_local = now + timedelta(seconds=seconds_to_ten_pm)
      eight_pm_reminder.apply_async(args=[user_id], eta=ten_pm_local)