from datetime import timedelta
from fruitfam.missions.rules.rule import Rule

class StreakMission(Rule):
  """
  A streak mission gives you points based on a streak. If the user reaches a
  specified streak, booty is awarded
  """
  def __init__(self, user_mission):
    super(StreakMission, self).__init__(user_mission)
  
  def streak_length(self):
    """
    How many days are we trying to hit?
    """
    pass
  
  def mission_type(self):
    return 'streak'
  
  def booty_earned(self, food_item):
    user_mission = self.get_user_mission()
    user = user_mission.user
    cur_streak = user.get_streak()
    last_upload = user.get_last_log_local()
    cur_user_time = user.local_time()
    last_upload_date = last_upload.date()
    cur_user_date = cur_user_time.date()
    if cur_user_date - last_upload_date == timedelta(days=1):
      # Increased the streak! Award some booty.
      booty_left_to_earn = self.target_booty() - user_mission.get_booty()
      streak_left_to_reach = self.streak_length() - cur_streak
      booty_to_award = int(booty_left_to_earn / float(streak_left_to_reach))
      return booty_to_award
    return 0