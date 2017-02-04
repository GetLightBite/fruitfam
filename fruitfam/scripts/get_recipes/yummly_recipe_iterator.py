import requests
import urllib

class Recipe(object):
  """Describes a yummly recipe"""
  def __init__(self, name, recipe_id, yield_amount, number_of_servings, img_url_1080, prep_time_seconds, ingredient_lines, calories, recipe_source_url):
    self.name = name
    self.recipe_id = recipe_id
    self.yield_amount = yield_amount
    self.number_of_servings = number_of_servings
    self.img_url_1080 = img_url_1080
    self.prep_time_seconds = prep_time_seconds
    self.ingredient_lines = ingredient_lines
    self.calories = calories
    self.recipe_source_url = recipe_source_url
    self.directions_list = None
    self.key_ingredient = None
    self.yummly_query = None
  
  def to_dict(self):
    return {
      'name' : self.name,
      'recipe_id' : self.recipe_id,
      'yield_amount' : self.yield_amount,
      'number_of_servings' : self.number_of_servings,
      'img_url_1080' : self.img_url_1080,
      'prep_time_seconds' : self.prep_time_seconds,
      'ingredient_lines' : self.ingredient_lines,
      'calories' : self.calories,
      'recipe_source_url' : self.recipe_source_url,
      'directions_list' : self.directions_list,
      'key_ingredient' : self.key_ingredient,
      'yummly_query' : self.yummly_query
    }
  
  @staticmethod
  def from_dict(self, rdict):
    name = rdict['name']
    recipe_id = rdict['recipe_id']
    yield_amount = rdict['yield_amount']
    number_of_servings = rdict['number_of_servings']
    img_url_1080 = rdict['img_url_1080']
    prep_time_seconds = rdict['prep_time_seconds']
    ingredient_lines = rdict['ingredient_lines']
    calories = rdict['calories']
    recipe_source_url = rdict['recipe_source_url']
    directions_list = rdict['directions_list']
    key_ingredient = rdict['key_ingredient']
    yummly_query = rdict['yummly_query']
    r = Recipe(name, recipe_id, yield_amount, number_of_servings, img_url_1080, prep_time_seconds, ingredient_lines, calories, recipe_source_url)
    r.directions_list = directions_list
    r.key_ingredient = key_ingredient
    r.yummly_query = yummly_query
    return r
  
  def __repr__(self):
    return '<Recipe %s>' % self.name.encode('utf-8')

class RecipeIterator(object):
  """Gives a bunch of recipes"""
  def __init__(self, searchterm, exclude_recipe_ids=[]):
    self.searchterm = searchterm
    self.base_url = 'http://api.yummly.com/v1/api/'
    self.app_id = '0d309a2b'
    self.app_key = '48abd826feb48c74649ad4ac063f8647'
    self.exclude_recipe_ids = exclude_recipe_ids
  
  def make_request(self, url):
    url = self.base_url + url
    if '?' in url:
      url += '&'
    else:
      url += '?'
    url += '_app_id=%s' % self.app_id
    url += '&_app_key=%s' % self.app_key
    resp = requests.get(url)
    return resp.json()
  
  def _get_recipe_ids(self, results, offset):
    url_escaped_search_term = urllib.quote(self.searchterm)
    url = 'recipes?q=%s&maxResult=%d&start=%d&requirePictures=true' % (url_escaped_search_term, results, offset)
    recipe_results = self.make_request(url)
    matches = recipe_results['matches']
    num_matches = recipe_results['totalMatchCount']
    recipe_ids = []
    for match in matches:
      recipe_id = match['id']
      recipe_ids.append(recipe_id)
    return num_matches, recipe_ids
  
  def _get_recipe_from_id(self, recipe_id):
    url = 'recipe/%s' % recipe_id
    recipe_data = self.make_request(url)
    images = recipe_data['images'][0]
    best_image = images['hostedLargeUrl']
    
    name = recipe_data['name']
    yield_amount = recipe_data['yield']
    number_of_servings = recipe_data['numberOfServings']
    img_1080 = best_image.replace('=s360', '=s1080')
    prep_time_seconds = recipe_data.get('prepTimeInSeconds', -1)
    ingredient_lines = recipe_data['ingredientLines']
    calories = -1
    try:
      calories = recipe_data['nutritionEstimates'][9]['value']
    except Exception as e:
      pass
    source_url = recipe_data['source']['sourceRecipeUrl']
    
    recipe = Recipe(name, recipe_id, yield_amount, number_of_servings, img_1080, prep_time_seconds, ingredient_lines, calories, source_url)
    return recipe
  
  def run(self):
    max_results = 99999
    offset = 0
    results_per_page = 150
    while offset <= max_results:
      cur_results_per_page = min(results_per_page, max_results - offset)
      num_matches, recipe_ids = self._get_recipe_ids(cur_results_per_page, offset)
      recipe_ids = filter(lambda x: x not in self.exclude_recipe_ids, recipe_ids)
      max_results = num_matches
      for recipe_id in recipe_ids:
        try:
          recipe = self._get_recipe_from_id(recipe_id)
          yield recipe
        except Exception as e:
          print 'passing due to %s' % e
          continue
      offset += results_per_page
      