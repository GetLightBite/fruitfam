from fruitfam.missions.rules.rule import Rule

class StreakMission(Rule):
  """
  A streak mission gives you points based on a streak. If the user reaches a
  specified streak, booty is awarded
  """
  def __init__(self, user_mission):
    super(StreakMission, self).__init__(user_mission)
  
  def get_mission_json(self):
    # Get normal json
    normal = super(StreakMission, self).get_mission_json()
    streak_mission = {
      'missionType' : 'streak'
    }
    normal['missionDetails'] = streak_mission
    return normal