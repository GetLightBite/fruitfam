from fruitfam.missions import rules

def get_users_rules(user_mission):
  cur_rules = get_rules(user_mission.mission_id)
  return cur_rules(user_mission)

def get_rules(mission_id):
  rules_list = level_progression()
  cur_rules = rules_list[mission_id - 1]
  return cur_rules

def level_progression():
  return [
    rules.level1.Level1,
    rules.level2.Level2,
    rules.level3.Level3
  ]*20