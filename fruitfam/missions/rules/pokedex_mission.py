from datetime import timedelta
from fruitfam.missions.rules.rule import Rule
from fruitfam.models.food_item import FoodItem

class PokedexMission(Rule):
  """
  A pokedex mission awards booty based on the number of items filled out of a list
  """
  def __init__(self, user_mission):
    super(PokedexMission, self).__init__(user_mission)
  
  def pokedex_card_images(self):
    """
    List of images for the pokedex cards, in order
    """
    pass
  
  def pokedex_conditions(self):
    """
    Returns a list of functions. Each function takes a food_item as an arg and
    returns a boolean indicating whether that food_item matching the
    corresponding pokedex item.
    """
    pass
  
  def pokedex_criteria(self):
    """
    Returns a list of strings which describe the criteria to match each pokedex
    item.
    """
    pass
  
  def get_progress(self):
    """
    Returns images to display in pokedex, with the number of matches
    """
    user_mission = self.get_user_mission()
    food_items = FoodItem.query.filter(
      FoodItem.user_id == user_mission.user_id
    ).filter(
      FoodItem.created > user_mission.created
    ).order_by(
      FoodItem.created
    ).all()
    
    image_urls = self.pokedex_card_images()
    num_matches = 0
    for i in range(self.pokedex_conditions()):
      condition = self.pokedex_conditions[i]
      for j in range(len(food_items)):
        food_item = food_items[j]
        if condition(food_items): # food item should go in the deck!
          image_urls[i] = food_item.diary_image()
          num_matches += 1
          break
    return image_urls, num_matches, len(image_urls)
        
  
  def is_match(self, food_item):
    # TODO(avadrevu): Return if a food item is a match. Check that no other food_items before it are matches - must be the first match for a given pokedex
    pass
  
  def mission_type(self):
    return 'pokedex'