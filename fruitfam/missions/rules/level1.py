from datetime import datetime, timedelta
from fruitfam.missions.rules.timeout_mission import TimeoutMission
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.common import date_to_datetime

class Level1(TimeoutMission):
  """Log a fruit in two minutes!"""
  def __init__(self, user_mission):
    super(Level1, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Mission 1' + Emoji.lightning()
  
  def rules_text(self):
    return [
      'You have 120 seconds to take a picture of a fruit and eat it!' + Emoji.hourglass()
    ]
  
  def mission_id(self):
    return 1
  
  def on_food_log(self, food_item):
    booty_earned = self.booty_earned(food_item)
    self.increment_booty(booty_earned)
    super(Level1, self).on_food_log(food_item)
  
  def booty_earned(self, food_item):
    return 20
  
  def target_booty(self):
    return 20
  
  def timeout(self):
    if self.get_timeouts_reached() == 0:
      return 120
    if self.get_timeouts_reached() > 0:
      # Get the end of the day
      user_local_time = self.get_user_mission().local_time()
      user_end_of_day = date_to_datetime(user_local_time.date()) + timedelta(days=1)
      user_time_to_eod = user_end_of_day - user_local_time
      seconds_to_eod = user_time_to_eod.seconds
      return seconds_to_eod
  
  def on_timeout_popup(self):
    return "Oh %s, looks like you ran out of time! But no worries, since it's your first mission we'll give you some extra time %s" % (Emoji.poo(), Emoji.wink())
  
  def booty_call(self):
    return 1
  
  def schedule_notifs(self):
    from fruitfam.taskslevel1_reminders import twenty_min_reminder, eight_pm_reminder
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
    if seconds_to_timeout > 4*60*60+40:
      seconds_to_eight_pm = seconds_to_timeout - 4*60*60
      eight_pm_local = now + timedelta(seconds=seconds_to_eight_pm)
      eight_pm_reminder.apply_async(args=[user_id], eta=eight_pm_local)
    elif seconds_to_timeout > 2*60*60:
      seconds_to_ten_pm = seconds_to_timeout - 2*60*60
      ten_pm_local = now + timedelta(seconds=seconds_to_ten_pm)
      eight_pm_reminder.apply_async(args=[user_id], eta=ten_pm_local)