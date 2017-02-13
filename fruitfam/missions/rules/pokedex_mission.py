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
    ).filter(
      FoodItem.not_food == False
    ).order_by(
      FoodItem.created
    ).all()
    
    image_urls = self.pokedex_card_images()
    images_with_id = [(x, None) for x in image_urls]
    found_match = [False]*len(images_with_id)
    num_matches = 0
    for i in range(len(self.pokedex_conditions())):
      condition = self.pokedex_conditions()[i]
      for j in range(len(food_items)):
        food_item = food_items[j]
        if (not found_match[i]) and condition(food_item): # food item should go in the deck!
          images_with_id[i] = (food_item.diary_img(), food_item.id)
          num_matches += 1
          found_match[i] = True
          break
    return images_with_id, num_matches, len(images_with_id)
        
  
  def is_match(self, food_item):
    # TODO(avadrevu): Return if a food item is a match. Check that no other food_items before it are matches - must be the first match for a given pokedex
    user_mission = self.get_user_mission()
    food_items = FoodItem.query.filter(
      FoodItem.user_id == user_mission.user_id
    ).filter(
      FoodItem.created > user_mission.created
    ).filter(
      FoodItem.created < food_item.created
    ).filter(
      FoodItem.not_food == False
    ).order_by(
      FoodItem.created
    ).all()
    print food_items
    conditions = self.pokedex_conditions()
    found_match = [False]*len(conditions)
    
    for i in range(len(food_items)):
      cur_food_item = food_items[i]
      for j in range(len(conditions)):
        condition = conditions[j]
        if (not found_match[j]) and condition(cur_food_item):
          found_match[j] = True
          break
    print found_match
    for j in range(len(conditions)):
      condition = conditions[j]
      if (not found_match[j]) and condition(food_item):
        return True
    return False
  
  def mission_type(self):
    return 'pokedex'
  
  def get_mission_json(self):
    # Get normal json
    normal = super(PokedexMission, self).get_mission_json()
    # Get Pokededx json
    progress, num_matches, total_items = self.get_progress()
    album = []
    for img_url, food_item_id in progress:
      album_item = {'thumbnailUrl' : img_url}
      if food_item_id != None:
        album_item['foodItemId'] = food_item_id
      album.append(album_item)
    pokedex_mission = {
      'progressDescription': '%d/%d' % (num_matches, total_items),
      'progressPercentage' : int(100*num_matches / float(total_items)),
      'timeRemaining': '',
      'album': album
    }
    normal['missionDetails'] = pokedex_mission
    return normal