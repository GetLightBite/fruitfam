from fruitfam.missions.rules.streak_mission import StreakMission
from fruitfam.utils.emoji import Emoji

class Level2(StreakMission):
  """Get a two day streak!"""
  def __init__(self, user_mission):
    super(Level2, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Mission 2' + Emoji.running_woman()
  
  def rules_text(self):
    return [
      "Congrats, you have a streak going! increase your streak to 2 by logging tomorrow " + Emoji.calendar()
    ]
  
  def mission_id(self):
    return 2
  
  def on_food_log(self, food_item):
    booty_earned = self.booty_earned(food_item)
    self.increment_booty(booty_earned)
    super(Level2, self).on_food_log(food_item)
  
  def streak_length(self):
    return 2
  
  def target_booty(self):
    return 100
  
  def booty_call(self):
    return 8