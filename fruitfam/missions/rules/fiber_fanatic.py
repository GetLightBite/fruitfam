from datetime import datetime, timedelta
from fruitfam.missions.rules.pokedex_mission import PokedexMission
from fruitfam.utils.emoji import Emoji
from fruitfam.utils.common import date_to_datetime

class FiberFanatic(PokedexMission):
  """Log all the fruits in the pokedex!"""
  def __init__(self, user_mission):
    super(FiberFanatic, self).__init__(user_mission)
  
  def mission_name(self):
    return 'Fiber Fanatic! ' + Emoji.poo()
  
  def rules_text(self):
    return [
      'Log 5 fibrous fruits!' + Emoji.trophy(),
      'Tap here to see the allowed fruits'
    ]
  
  def explanation(self):
    return 'Log 5 of the following 6 fruits: Passion fruit, Avacado, Raspberries, Kumquats, Guavas, Blackberries'
  
  def mission_id(self):
    return 3
  
  def on_food_log(self, food_item):
    booty_earned = self.booty_earned(food_item)
    self.increment_booty(booty_earned)
  
  def booty_earned(self, food_item):
    if self.is_match(food_item):
      return 100
    return 0
  
  def target_booty(self):
    return 500
  
  def pokedex_card_images(self):
    return [
      'https://s3.amazonaws.com/fruitfam/passionfruitCell.png',
      'https://s3.amazonaws.com/fruitfam/avocadoCell.png',
      'https://s3.amazonaws.com/fruitfam/raspberryCell.png',
      'https://s3.amazonaws.com/fruitfam/kumquatCell.png',
      'https://s3.amazonaws.com/fruitfam/guavaCell.png',
      'https://s3.amazonaws.com/fruitfam/blackberryCell.png'
    ]
  
  def pokedex_conditions(self):
    return [
      lambda x: x.component_id == 41,
      lambda x: x.component_id == 3,
      lambda x: x.component_id == 52,
      lambda x: x.component_id == 24,
      lambda x: x.component_id == 21,
      lambda x: x.component_id == 5,
    ]
  
  def pokedex_criteria(self):
    return [
      'Log a Passion fruit',
      'Log an Avocado',
      'Log a Raspberry',
      'Log a Kumquat',
      'Log a Guava',
      'Log a Blackberry'
    ]
  
  def booty_call(self):
    return 26
  
  def introduction(self):
    return [
      "Congratulations! You're well on your way to becoming a fruit king " + Emoji.crown(),
      "The next mission is about fiber. We'll show you what to eat to lower cholesterol, achieve a healthy weight, and of course, normalize bowel movements " + Emoji.poo()
    ]
  
  def schedule_notifs(self):
    pass