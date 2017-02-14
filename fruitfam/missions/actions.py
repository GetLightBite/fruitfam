from fruitfam.missions.rules import fiber_fanatic
from fruitfam.missions.rules import hard_pokedex
from fruitfam.missions.rules import level1
from fruitfam.missions.rules import level2
from fruitfam.missions.rules import level3
from fruitfam.missions.rules import simple_pokedex

def get_users_rules(user_mission):
  cur_rules = get_rules(user_mission.mission_id)
  return cur_rules(user_mission)

def get_rules(mission_id):
  rules_list = level_progression()
  cur_rules = rules_list[mission_id - 1]
  return cur_rules

def level_progression():
  return [
    level1.Level1,
    simple_pokedex.SimplePokedex,
    fiber_fanatic.FiberFanatic,
    hard_pokedex.HardPokedex,
    level3.Level3
  ]*20