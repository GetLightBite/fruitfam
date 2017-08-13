from clarifai.rest import ClarifaiApp
import json
from fruitfam.models.component import Component
from fruitfam.scripts.test_svm.clarifai_test import ClarifaiTest
from fruitfam.scripts.test_svm.test import Test
import numpy as np
from sklearn import preprocessing
from sklearn.externals import joblib

class SVMTest(Test):
  """Runs a test with an SVM"""
  def __init__(self, image_to_components, svm_location, clarifai_tags_location):
    super(SVMTest, self).__init__(image_to_components)
    self.svm_location = svm_location
    self.clarifai_tags_location = clarifai_tags_location
    self.all_components = Component.query.all()
    self.list_of_clarifai_tags = []
    self.le = None
  
  def run(self):
    # first get clarifai results
    ct = ClarifaiTest()
    clarifai_results = ct.lookup(self.images)
    
    # Now load up the SVM
    k = open(self.clarifai_tags_location, 'r')
    list_of_clarifai_tags = json.loads(k.read())
    self.list_of_clarifai_tags = list_of_clarifai_tags
    k.close()
    le = preprocessing.LabelEncoder()
    le.fit(list_of_clarifai_tags)
    self.le = le
    clf = joblib.load(self.svm_location)
    
    # Make SVM predictions!
    comp_guesses = self.clarifai_tags_to_components_list(clarifai_results, clf)
    self.image_to_results = comp_guesses
    return comp_guesses
  
  def clarifai_tags_to_components_list(self, all_clarifai_tags, clf):
    all_components = self.all_components
    all_components.sort(key=lambda x: x.id)
    
    out = {}
    for image_url in all_clarifai_tags:
      clarifai_tags = all_clarifai_tags[image_url]
      if clarifai_tags == None:
        return None
      vector = self.tags_to_vector(clarifai_tags)
      probs = list(clf.predict_log_proba([vector])[0])
      lowest_score = min(probs)
      probs += [lowest_score-1]*(len(all_components) - len(probs))
      probs_with_tags = zip(probs, all_components)
      probs_with_tags.sort(reverse=True)
      components_in_order = map(lambda x: x[1], probs_with_tags)
      out[image_url] = components_in_order[0].id
    return out
  
  def tags_to_vector(self, clarifai_tags):
    num_classes=len(self.list_of_clarifai_tags)
    zeros = np.zeros(num_classes)
    [tags, scores] = zip(*clarifai_tags)
    known_tags = set(self.le.classes_)
    filtered_tags = set(tags).intersection(known_tags)
    indexes = self.le.transform(list(filtered_tags))
    zeros[indexes] = np.array(scores)
    return zeros