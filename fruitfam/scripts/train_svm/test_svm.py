from clarifai.rest import ClarifaiApp
import json
import numpy as np
import os
from sklearn import preprocessing
from sklearn.externals import joblib
import sys

# add parent dir to PYTHONPATH
cur_path = os.path.abspath('../../..')
sys.path.insert(1, cur_path)
from fruitfam.models.component import Component

k = open('/users/avadrevu/workspace/fruitfam/fruitfam/bin/filtered_svm/clarifai_tags_filtered.json', 'r')
clarifai_tags_str = k.read()
k.close()

list_of_clarifai_tags = json.loads(clarifai_tags_str)
list_of_clarifai_tags.sort()

le = preprocessing.LabelEncoder()
le.fit(list_of_clarifai_tags)

clf = joblib.load('/users/avadrevu/workspace/fruitfam/fruitfam/bin/filtered_svm/svm_filtered.pkl')

def tags_to_vector(clarifai_tags, num_classes=len(list_of_clarifai_tags)):
  zeros = np.zeros(num_classes)
  [tags, scores] = zip(*clarifai_tags)
  indexes = le.transform(list(tags))
  zeros[indexes] = np.array(scores)
  return zeros

def clarifai_tags_to_components_list(clarifai_tags):
  all_components = Component.query.all()
  all_components.sort(key=lambda x: x.id)
  if clarifai_tags == None:
    return None
  vector = tags_to_vector(clarifai_tags)
  probs = list(clf.predict_log_proba(vector)[0])
  lowest_score = min(probs)
  probs += [lowest_score-1]*(len(all_components) - len(probs))
  probs_with_tags = zip(probs, all_components)
  probs_with_tags.sort(reverse=True)
  components_in_order = map(lambda x: x[1], probs_with_tags)
  return components_in_order

# Start making Clarifai guess things!
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
  print e


url = 'http://analyze.life/wellbeing.support/wp-content/uploads/2015/07/apples.jpg'
c_result = clarifai_app.tag_urls(urls=[url], model='food-items-v1.0')
predicted_concepts = c_result['outputs'][0]['data']['concepts']
prediction_scores = [(x['name'], x['value']) for x in predicted_concepts]

comp_guesses = clarifai_tags_to_components_list(prediction_scores)
print comp_guesses