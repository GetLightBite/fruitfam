from datetime import datetime, timedelta
from fruitfam.missions.rules.pokedex_mission import PokedexMission
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.common import date_to_datetime

class HardPokedex(PokedexMission):
  """Log all the fruits in the pokedex!"""
  def __init__(self, user_mission):
    super(HardPokedex, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Log these %s fruits!' % Emoji.six()
  
  def rules_text(self):
    return [
      'Tap here to find out the fruits to log!' + Emoji.right_arrow()
    ]
  
  def explanation(self):
    return 'Log each of the following fruits: Papaya, Mango, Kiwi, Apple, Orange, and Banana!'
  
  def mission_id(self):
    return 4
  
  def on_food_log(self, food_item):
    booty_earned = self.booty_earned(food_item)
    self.increment_booty(booty_earned)
  
  def booty_earned(self, food_item):
    if self.is_match(food_item):
      return 150
    return 0
  
  def target_booty(self):
    return 750
  
  def pokedex_card_images(self):
    return [
      'https://s3.amazonaws.com/fruitfam/papayaCell.png',
      'https://s3.amazonaws.com/fruitfam/mangoCell.png',
      'https://s3.amazonaws.com/fruitfam/kiwiCell.png',
      'https://s3.amazonaws.com/fruitfam/redAppleCell.png',
      'https://s3.amazonaws.com/fruitfam/orangeCell.png',
      'https://s3.amazonaws.com/fruitfam/bananaCell.png'
    ]
  
  def pokedex_conditions(self):
    return [
      lambda x: x.component_id == 40,
      lambda x: x.component_id == 28,
      lambda x: x.component_id == 23,
      lambda x: x.component_id == 1,
      lambda x: x.component_id in [35, 36, 37, 38, 39],
      lambda x: x.component_id == 4
    ]
  
  def pokedex_criteria(self):
    return [
      'Log a Papaya',
      'Log a Mango',
      'Log a Kiwi',
      'Log an Apple',
      'Log an Orange',
      'Log a Banana'
    ]
  
  def booty_call(self):
    return 47
  
  def schedule_notifs(self):
    pass