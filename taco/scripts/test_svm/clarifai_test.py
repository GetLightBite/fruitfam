from clarifai.rest import ClarifaiApp
import itertools
import json
import os

class ClarifaiTest(object):
  """
  Returns clarifai results for any image. Stores results in a cache
  Cache is a json file - `clarifai_cache.json`
  Uses separate keys to main app
  
  
  Other app_id/app_secret combos to use:
  
  LY9bwK2ycmOnf57aqpdhOvaT2tw9l7hVOYkMuxB3
  3t2uoDSclfx97t_s4e1GoK9EPNHOduWHjyvNVy0u
  
  3e3DrOKoii5AhOO79dK-UCOYoLZwOP0AlY9uYmo7
  T8ENsrSO4K4Y3tWVvtlZBCAeKOmUfSjHzsu7G-h9
  
  DGrKEGiG9qYiFo6QXap5P1aAJ_mXvDhrsIGPy3uX
  QiUQZENNSWvPSZUykP3XIh2XQ6P0AjcduaT1uDma
  """
  def __init__(self,
    app_id='DGrKEGiG9qYiFo6QXap5P1aAJ_mXvDhrsIGPy3uX',
    app_secret='QiUQZENNSWvPSZUykP3XIh2XQ6P0AjcduaT1uDma'):
    self.app_id = app_id
    self.app_secret = app_secret
    self.cache_location = 'fruitfam/scripts/test_svm/clarifai_cache.json'
    os.environ["CLARIFAI_APP_ID"] = app_id
    os.environ["CLARIFAI_APP_SECRET"] = app_secret
    
    self.clarifai_app = ClarifaiApp()
  
  def grouper(self, n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(*args, fillvalue=fillvalue)
  
  def get_cache(self):
    search_results_file = open(self.cache_location, 'r')
    search_results = json.loads(search_results_file.read())
    search_results_file.close()
    return search_results
  
  def write_to_cache(self, somedict):
    cur_dict = self.get_cache()
    cur_dict.update(somedict)
    search_results_file = open(self.cache_location, 'w')
    search_results_file.write(json.dumps(cur_dict))
    search_results_file.close()
  
  def get_cached_results(self, images):
    cache = self.get_cache()
    out = {}
    for image in images:
      if image in cache:
        out[image] = cache[image]
    return out
  
  def lookup_clarifai(self, images):
    url_groups = list(self.grouper(128, images))
    results = {}
    for urls in url_groups:
      urls = list(filter(None, urls))
      print len(urls)
      print urls
      c_result = self.clarifai_app.tag_urls(urls=urls, model='food-items-v1.0')
      results_data = c_result['outputs']
      for result_data in results_data:
        input_url = result_data['input']['data']['image']['url']
        predicted_concepts = result_data['data']['concepts']
        prediction_scores = [(x['name'], x['value']) for x in predicted_concepts]
        results[input_url] = prediction_scores
      self.write_to_cache(results)
    return results
  
  def lookup(self, images):
    cached_results = self.get_cached_results(images)
    non_cached_images = [x for x in images if x not in cached_results]
    clarifai_results = self.lookup_clarifai(non_cached_images)
    cached_results.update(clarifai_results)
    self.write_to_cache(cached_results)
    return cached_results