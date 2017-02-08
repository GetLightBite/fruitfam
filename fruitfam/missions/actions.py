from fruitfam.missions.rules.level1 import Level1

def get_users_rules(user_mission):
  cur_rules = get_rules(user_mission.mission_id)
  return cur_rules(user_mission)

def get_rules(mission_id):
  print mission_id
  rules_list = level_progression()
  cur_rules = rules_list[mission_id - 1]
  return cur_rules

def level_progression():
  return [
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
    Level1,
    Level1,
    Level1,
  ]