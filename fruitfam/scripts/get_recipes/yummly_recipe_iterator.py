import requests
import urllib

class RecipeIterator(object):
  """Gives a bunch of recipes"""
  def __init__(self, searchterm):
    self.searchterm = searchterm
    self.base_url = 'http://api.yummly.com/v1/api/'
    self.app_id = '0d309a2b'
    self.app_key = '48abd826feb48c74649ad4ac063f8647'
    
  
  def __iter__(self):
    return self
  
  def make_request(self, url):
    url = self.base_url + url
    url += '&app_id=%s' % self.app_id
    url += '&app_key=%s' % self.app_key
    resp = requests.get(url)
    return resp.json()
  
  def _get_recipe_ids(self, results, offset):
    url_escaped_search_term = urllib.quote(self.searchterm)
    url = 'recipes?q=%s&maxResult=%d&start=%d&requirePictures=true' % (url_escaped_search_term, results, offset)
    recipe_results = self.make_request(url)
    matches = recipe_results['matches']
    for match in matches:
      recipe_id = match['id']
      yield recipe_id
  
  def function():
    pass
  
  def next(self):
    pass