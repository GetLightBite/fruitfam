from datetime import datetime, timedelta
from fruitfam.missions.rules.pokedex_mission import PokedexMission
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.common import date_to_datetime

class SimplePokedex(PokedexMission):
  """Log all the fruits in the pokedex!"""
  def __init__(self, user_mission):
    super(PokedexMission, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Collect all the fruits!' + Emoji.lightning()
  
  def rules_text(self):
    return [
      'Log an Apple, and Orange and a Banana to complete this mission!' + Emoji.hourglass()
    ]
  
  def mission_id(self):
    return 2
  
  def on_food_log(self, food_item):
    booty_earned = self.booty_earned(food_item)
    print 'booty_earned', booty_earned
    self.increment_booty(booty_earned)
  
  def booty_earned(self, food_item):
    if self.is_match(food_item):
      return 100
    return 0
  
  def target_booty(self):
    return 300
  
  def pokedex_card_images(self):
    return [
      'https://s3.amazonaws.com/fruitfam/bananaCell.png',
      'https://s3.amazonaws.com/fruitfam/orangeCell.png',
      'https://s3.amazonaws.com/fruitfam/redAppleCell.png'
    ]
  
  def pokedex_conditions(self):
    return [
      lambda x: x.component_id == 4,
      lambda x: x.component_id in [35, 36, 37, 38, 39],
      lambda x: x.component_id ==1
    ]
  
  def pokedex_criteria(self):
    return [
      'Log a Banana',
      'Log an Orange',
      'Log an Apple'
    ]
  
  def booty_call(self):
    return 12
  
  def schedule_notifs(self):
    pass