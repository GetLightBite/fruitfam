# import requests
# import urllib

# class Recipe(object):
#   """Describes a yummly recipe"""
#   def __init__(self, name, recipe_id, yield_amount, number_of_servings, img_url_1080, prep_time_seconds, ingredient_lines, calories, recipe_source_url):
#     self.name = name
#     self.recipe_id = recipe_id
#     self.yield_amount = yield_amount
#     self.number_of_servings = number_of_servings
#     self.img_url_1080 = img_url_1080
#     self.prep_time_seconds = prep_time_seconds
#     self.ingredient_lines = ingredient_lines
#     self.calories = calories
#     self.recipe_source_url = recipe_source_url

# class RecipeIterator(object):
#   """Gives a bunch of recipes"""
#   def __init__(self, searchterm):
#     self.searchterm = searchterm
#     self.base_url = 'http://api.yummly.com/v1/api/'
#     self.app_id = '0d309a2b'
#     self.app_key = '48abd826feb48c74649ad4ac063f8647'
    
  
#   def __iter__(self):
#     return self
  
#   def make_request(self, url):
#     url = self.base_url + url
#     url += '&app_id=%s' % self.app_id
#     url += '&app_key=%s' % self.app_key
#     resp = requests.get(url)
#     return resp.json()
  
#   def _get_recipe_ids(self, results, offset):
#     url_escaped_search_term = urllib.quote(self.searchterm)
#     url = 'recipes?q=%s&maxResult=%d&start=%d&requirePictures=true' % (url_escaped_search_term, results, offset)
#     recipe_results = self.make_request(url)
#     matches = recipe_results['matches']
#     num_matches = recipe_results['totalMatchCount']
#     recipe_ids = []
#     for match in matches:
#       recipe_id = match['id']
#       recipe_ids.append(recipe_id)
#     return num_matches, recipe_ids
  
#   def _get_recipe_data_from_id(self, recipe_id):
#     url = 'recipe/%s' % recipe_id
#     recipe_data = self.make_request(url)
#     images = recipe_data['images']
#     best_image = images['hostedLargeUrl']
    
#     name = recipe_data['name']
#     yield_amount = recipe_data['yield']
#     number_of_servings = recipe_data['numberOfServings']
#     img_1080 = best_image.replace('=s360', '=s1080')
#     prep_time_seconds = recipe_data['prepTimeInSeconds']
#     ingredient_lines = recipe_data['ingredientLines']
#     calories = recipe_data['nutritionEstimates'][9]['value']
#     source_url = recipe_data['source']['sourceRecipeUrl']
    
#     recipe = Recipe(name, yield_amount, number_of_servings, img_1080, prep_time_seconds, ingredient_lines, calories, source_url)
#     return recipe
  
#   def next(self):
#     max_results = 99999
#     offset = 0
#     results_per_page = 50
#     while offset < max_results:
#       cur_results_per_page = min(results_per_page, max_results - offset)
#       num_matches, recipe_ids = self._get_recipe_ids(50, 0)
    
#       