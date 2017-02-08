from fruitfam.missions.rules.level1 import Level1
from fruitfam.missions.rules.level2 import Level2

def get_users_rules(user_mission):
  cur_rules = get_rules(user_mission.mission_id)
  return cur_rules(user_mission)

def get_rules(mission_id):
  rules_list = level_progression()
  cur_rules = rules_list[mission_id - 1]
  return cur_rules

def level_progression():
  return [
    Level1,
    Level2,
    Level1,
    Level2,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
    Level1,
  ]