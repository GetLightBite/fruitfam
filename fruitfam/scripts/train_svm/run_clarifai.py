from clarifai.rest import ClarifaiApp
import itertools
import json
import os
import operator

os.environ["CLARIFAI_APP_ID"] = "LY9bwK2ycmOnf57aqpdhOvaT2tw9l7hVOYkMuxB3"
os.environ["CLARIFAI_APP_SECRET"] = "3t2uoDSclfx97t_s4e1GoK9EPNHOduWHjyvNVy0u"

clarifai_app, food_model = None, None
try:
  print 'starting clarifai app...'
  clarifai_app = ClarifaiApp()
  # food_model = clarifai_app.models.get('food-items-v1.0')
  print 'clarifai set up complete!'
except Exception as e:
  print "Had an issue with launching Clarifai!!!"

def grouper(n, iterable, fillvalue=None):
  "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
  args = [iter(iterable)] * n
  return itertools.izip_longest(*args, fillvalue=fillvalue)

search_results_file = open('search_results.json', 'r')
search_results = json.loads(search_results_file.read())
search_results_file.close()
# TODO: filter out results from images_to_filter_out.json


urls = reduce(operator.add, search_results.values())
urls = filter(None, urls)
print 'Analyzing %d images' % len(urls)

# max batch size is 128
url_groups = list(grouper(128, urls))

doc = open('clarifai_results.json', 'r')
parsed_results = json.loads(doc.read())
doc.close()


for urls in url_groups:
  urls = list(filter(None, urls))
  c_result = clarifai_app.tag_urls(urls=urls, model='food-items-v1.0')
  results_data = c_result['outputs']
  for result_data in results_data:
    input_url = result_data['input']['data']['image']['url']
    predicted_concepts = result_data['data']['concepts']
    prediction_scores = [(x['name'], x['value']) for x in predicted_concepts]
    parsed_results[input_url] = prediction_scores
  # save
  doc = open('clarifai_results.json', 'w')
  doc.write(json.dumps(parsed_results))
  doc.close()