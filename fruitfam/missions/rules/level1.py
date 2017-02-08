from fruitfam.missions.rules.timeout_mission import TimeoutMission
from fruitfam.utils.emoji import Emoji

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
      return 12*60*60 # 12 more hours
  
  def on_timeout_popup(self):
    return "Oh %s, looks like you ran out of time! But no worries, since it's your first mission we'll give you some extra time %s" % (Emoji.poo(), Emoji.wink())
  
  def booty_call(self):
    return 1