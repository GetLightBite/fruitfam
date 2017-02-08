from fruitfam.missions.rules.streak_mission import StreakMission
from fruitfam.utils.emoji import Emoji

class Level3(StreakMission):
  """Get a five day streak!"""
  def __init__(self, user_mission):
    super(Level3, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Mission 3' + Emoji.fire()
  
  def rules_text(self):
    streak = self.get_user_mission().user.get_streak()
    return [
      "Log fruits for five %s days in a row to complete this mission! %s %d/5 complete!" (Emoji.hand(), Emoji.calendar(), streak)
    ]
  
  def mission_id(self):
    return 2
  
  def on_food_log(self, food_item):
    booty_earned = self.booty_earned(food_item)
    self.increment_booty(booty_earned)
    super(Level3, self).on_food_log(food_item)
  
  def streak_length(self):
    return 5
  
  def target_booty(self):
    return 300
  
  def booty_call(self):
    return 20