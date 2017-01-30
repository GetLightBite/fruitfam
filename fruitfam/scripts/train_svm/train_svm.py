import json
import numpy as np
import operator
import os
import random
from sklearn import preprocessing
from sklearn import svm
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
import sys

# add parent dir to PYTHONPATH
cur_path = os.path.abspath('../../..')
sys.path.insert(1, cur_path)
from fruitfam.models.component import Component

# get mapping of fruit_name => list of clarifai results
uploaded_images_file = open('search_results.json', 'r')
uploaded_images = json.loads(uploaded_images_file.read())
uploaded_images_file.read()
clarifai_tags_file = open('clarifai_results.json', 'r')
clarifai_tags = json.loads(clarifai_tags_file.read())
clarifai_tags_file.close()

# Get the mapping from fruit name to clarifai tag
fruit_to_tags_mapping = {}
for fruit in uploaded_images:
  urls = uploaded_images[fruit]
  for url in urls:
    if url != None:
      url_tags = clarifai_tags.get(url, None)
      cur_tags = fruit_to_tags_mapping.get(fruit, [])
      cur_tags.append(url_tags)
      fruit_to_tags_mapping[fruit] = cur_tags

# Get a list of all clarifai tags
all_clarifai_tags = set()
for fruit in fruit_to_tags_mapping:
  clarifai_tags = fruit_to_tags_mapping[fruit]
  for tag_list in clarifai_tags:
    for tag in tag_list:
      all_clarifai_tags.add(tag[0])

all_clarifai_tags = list(all_clarifai_tags)
all_clarifai_tags.sort()
le = preprocessing.LabelEncoder()
le.fit(all_clarifai_tags)

# train the SVM on all the data
def tags_to_vector(clarifai_tags, num_classes=len(all_clarifai_tags)):
  zeros = np.zeros(num_classes)
  [tags, scores] = zip(*clarifai_tags)
  indexes = le.transform(list(tags))
  zeros[indexes] = np.array(scores)
  return zeros

comps = Component.query.all()
X, y = [], []
for component in comps:
  comp_id = component.id
  comp_name = component.name
  clarifai_tags_list = fruit_to_tags_mapping[comp_name]
  for clarifai_tags in clarifai_tags_list:
    vector = tags_to_vector(clarifai_tags)
    X.append(vector)
    y.append(comp_id)

print X[0:2]
print y[0:2]

X = np.array(X)
y = np.array(y)

clf_weights = LogisticRegression()
clf_weights.fit(X, y)

joblib.dump(clf_weights, '/users/avadrevu/workspace/fruitfam/fruitfam/bin/svm.pkl')
names_json = json.dumps(all_clarifai_tags)
k = open('/users/avadrevu/workspace/fruitfam/fruitfam/bin/clarifai_tags.json', 'w')
k.write(names_json)
k.close()

sys.exit(0)