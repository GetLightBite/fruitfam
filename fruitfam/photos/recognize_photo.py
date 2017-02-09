from clarifai.rest import ClarifaiApp
import cStringIO
import json
import io
import os
import numpy as np
from PIL import Image
from sklearn import preprocessing
from sklearn.externals import joblib
from fruitfam.models.component import Component

os.environ["CLARIFAI_APP_ID"] = "kjYQw3CwWsbSbQ_jz8hKQdKjQyEU-xp7-2l0Sf4H"
os.environ["CLARIFAI_APP_SECRET"] = "w0tRU0zEat5rwuX91GRP4ugXIpxqvZB-q-guqgnL"

########################################
# Set up reusable data in global scope #
########################################

clarifai_app, food_model, general_model = None, None, None
try:
  print 'starting clarifai app...'
  clarifai_app = ClarifaiApp()
  food_model = clarifai_app.models.get('food-items-v1.0')
  general_model = clarifai_app.models.get('general-v1.3')
  print 'clarifai set up complete!'
except Exception as e:
  print "Had an issue with launching Clarifai!!!"

k = open('fruitfam/bin/clarifai_tags.json', 'r')
clarifai_tags_str = k.read()
k.close()

list_of_clarifai_tags = json.loads(clarifai_tags_str)
list_of_clarifai_tags.sort()

le = preprocessing.LabelEncoder()
le.fit(list_of_clarifai_tags)

clf = joblib.load('fruitfam/bin/svm.pkl')

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

def img_data_to_img_object(image_data):
  stream_data = image_data.stream.read()
  img_data = cStringIO.StringIO(stream_data)
  img = Image.open(img_data)
  return img

def guess_components(img):
  global food_model
  global general_model
  if img == None:
    return [Component.query.first()], []
  img_byte_arr = io.BytesIO()
  img.save(img_byte_arr, format='JPEG')
  img_bytes = img_byte_arr.getvalue()
  
  food_clarifai_tags = get_clarifai_guess_from_bytes(img_bytes, food_model)
  general_clarifai_tags = get_clarifai_guess_from_bytes(img_bytes, general_model)
  image_type = infer_image_type(general_clarifai_tags)
  tags_to_return = food_clarifai_tags if image_type == 'food' else general_clarifai_tags
  components_guesses = clarifai_tags_to_components_list(food_clarifai_tags)
  return image_type, components_guesses, tags_to_return

def infer_image_type(general_clarifai_tags):
  human_tags = ['person', 'man', 'woman', 'face', 'nose', 'ear', 'glasses', 'pretty', 'smile', 'sexy', 'girl', 'boy', 'child', 'baby', 'human', 'people', 'men', 'women', 'children', 'faces']
  for classification, prob in general_clarifai_tags:
    if prob > 0.9:
      if classification in human_tags:
        return 'person'
  return 'food'

def get_clarifai_guess_from_bytes(img_bytes, model):
  resp = model.predict_by_bytes(img_bytes)
  out = []
  try:
    results = resp['outputs'][0]['data']['concepts']
    for result in results:
      prob = result['value']
      classification = result['name']
      out.append((classification, prob))
  except Exception as e:
    return None
  return out