import os
os.environ["APP_CONFIG_FILE"] = "../config/devel.py"

from fruitfam import db
from fruitfam.models.component import Component
from fruitfam.models.recipe import Recipe
from fruitfam.scripts.get_recipes.yummly_recipe_iterator import Recipe as YRecipe
from fruitfam.utils.upload_image import upload_image
import json

def get_all_recipes():
  k = open('fruitfam/scripts/get_recipes/recipe_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  return recipe_list

def add_recipe_to_uploaded_list(recipe):
  k = open('fruitfam/scripts/get_recipes/uploaded_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  recipe_list.append(recipe.recipe_id)
  
  recipe_list_text = json.dumps(recipe_list)
  k = open('fruitfam/scripts/get_recipes/uploaded_list.json', 'w')
  k.write(recipe_list_text)
  k.close()

def is_in_uploaded_list(recipe):
  k = open('fruitfam/scripts/get_recipes/uploaded_list.json', 'r')
  recipe_list_text = k.read()
  k.close()
  recipe_list = json.loads(recipe_list_text)
  return recipe.recipe_id in recipe_list

components = Component.query.all()
comp_name_to_component = {x.name: x for x in components}

recipes = get_all_recipes()
for recipe in recipes:
  r = YRecipe.from_dict(recipe)
  if not is_in_uploaded_list(r):
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
    # Get component
    comp = comp_name_to_component[key_ingredient]
    # Upload image to aws
    aws_url = upload_image(img_url_1080, 1810, is_square=False)
    try:
      new_recipe = Recipe(name, comp, recipe_id, yield_amount, number_of_servings, aws_url, prep_time_seconds, ingredient_lines, calories, recipe_source_url, directions_list, key_ingredient, yummly_query)
      db.session.add(new_recipe)
      db.session.commit()
    except Exception as e:
      continue
    # Add to uploaded list
    add_recipe_to_uploaded_list(r)
    print 'added recipe'
    print r
    print aws_url

