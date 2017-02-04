import os
os.environ["APP_CONFIG_FILE"] = "../config/devel.py"

# from fruitfam.models.component import Component
# from fruitfam.models.recipe import Recipe
from fruitfam.scripts.get_recipes.yummly_recipe_iterator import Recipe as YRecipe
import json

def get_all_recipes():
  k = open('recipe_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  return recipe_list

recipes = get_all_recipes()
for recipe in recipes:
  r = YRecipe.from_dict(recipe)
  name = r.name
  recipe_id = r.recipe_id
  yield_amount = r.yield_amount
  number_of_servings = r.number_of_servings
  img_url_1080 = r.img_url_1080
  prep_time_seconds = r.prep_time_seconds if r.prep_time_seconds != -1 else None
  ingredient_lines = r.ingredient_lines
  calories = r.calories if r.calories != -1 else None
  recipe_source_url = r.recipe_source_url
  directions_list = r.directions_list
  key_ingredient = r.key_ingredient
  yummly_query = r.yummly_query
  print r.name
  print r.img_url_1080
  print ''

