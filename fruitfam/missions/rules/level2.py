from fruitfam.missions.rules.timeout_mission import TimeoutMission
from fruitfam.utils.emoji import Emoji

class Level2(TimeoutMission):
  """Log two fruits in two hours!"""
  def __init__(self, user_mission):
    super(Level2, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Mission 2' + Emoji.lightning()
  
  def rules_text(self):
    return [
      "Congrats, you have a streak going! increase your streak to 2 by logging tomorrow " + Emoji.hourglass()
    ]
  
  def mission_id(self):
    return 2
  
  def on_food_log(self, food_item):
    booty_earned = self.booty_earned(food_item)
    self.increment_booty(booty_earned)
    super(Level2, self).on_food_log(food_item)
  
  def booty_earned(self, food_item):
    return 50
  
  def target_booty(self):
    return 100
  
  def mission_type(self):
    return 'timed'
  
  def timeout(self):
    if self.get_timeouts_reached() == 0:
      return 60*60*2
    if self.get_timeouts_reached() > 0:
      return 12*60*60 # 12 more hours
  
  def on_timeout_popup(self):
    return "Oh %s, looks like you ran out of time! But no worries, since it's your second mission we'll give you some extra time %s" % (Emoji.poo(), Emoji.wink())
  
  def booty_call(self):
    return 3