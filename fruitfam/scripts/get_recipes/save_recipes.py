from directions_from_recipe_website import *
import json
from yummly_recipe_iterator import *


def save_new_recipe(recipe):
  k = open('recipe_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  recipe_dict = recipe.to_dict()
  recipe_list.append(recipe_dict)
  recipe_list_text = json.dumps(recipe_list)
  k = open('recipe_list.json', 'w')
  k.write(recipe_list_text)
  k.close()

def get_num_results_saved(query):
  k = open('recipe_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  i = 0
  for recipe in recipe_list:
    if recipe['yummly_query'] == query:
      i += 1
  return i

def is_result(recipe_source_url):
  k = open('recipe_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  for recipe in recipe_list:
    if recipe['recipe_source_url'] == recipe_source_url:
      return True
  return False

def all_recipe_ids():
  k = open('recipe_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  recipe_ids = []
  for recipe in recipe_list:
    recipe_ids.append(recipe['recipe_id'])
  return recipe_ids

def save_recipes(ingredient, search_term, num_results):
  if num_results <= 0:
    return
  cur_ids = all_recipe_ids()
  ri = RecipeIterator(search_term, cur_ids)
  i=0
  for recipe in ri.run():
    if i == num_results:
      break
    if is_result(recipe.recipe_source_url):
      continue
    directions = get_directions_from_url(recipe.recipe_source_url)
    if directions != None:
      recipe.directions_list = directions
      recipe.key_ingredient = ingredient
      recipe.yummly_query = search_term
      save_new_recipe(recipe)
      print 'search for %s yeilded:' % search_term
      print recipe
      print ''
      i += 1