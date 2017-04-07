import base64
from clarifai.rest import ClarifaiApp
import cStringIO
from fruitfam.models.component import Component
from fruitfam.utils.parallel_requester import ParallelRequester
import io
import json
import numpy as np
import os
from PIL import Image
import requests
from sklearn import preprocessing
from sklearn.externals import joblib
import time

CLARIFAI_APP_ID = "kjYQw3CwWsbSbQ_jz8hKQdKjQyEU-xp7-2l0Sf4H"
CLARIFAI_APP_SECRET = "w0tRU0zEat5rwuX91GRP4ugXIpxqvZB-q-guqgnL"

data = {'grant_type': 'client_credentials'}
auth = (CLARIFAI_APP_ID, CLARIFAI_APP_SECRET)
authurl = 'https://api.clarifai.com/v2/token'
res = requests.post(authurl, auth=auth, data=data)
CLARIFAI_AUTH_TOKEN = res.json()['access_token']

########################################
# Set up reusable data in global scope #
########################################

k = open('fruitfam/bin/clarifai_tags.json', 'r')
clarifai_tags_str = k.read()
k.close()

list_of_clarifai_tags = json.loads(clarifai_tags_str)
list_of_clarifai_tags.sort()

le = preprocessing.LabelEncoder()
le.fit(list_of_clarifai_tags)

clf = joblib.load('fruitfam/bin/svm.pkl')

all_components = Component.query.all()
all_components.sort(key=lambda x: x.id)

def tags_to_vector(clarifai_tags, num_classes=len(list_of_clarifai_tags)):
  zeros = np.zeros(num_classes)
  [tags, scores] = zip(*clarifai_tags)
  known_tags = set(le.classes_)
  filtered_tags = set(tags).intersection(known_tags)
  indexes = le.transform(list(filtered_tags))
  zeros[indexes] = np.array(scores)
  return zeros

def clarifai_tags_to_components_list(clarifai_tags):
  global all_components
  if clarifai_tags == None:
    return None
  some_comp = find_top_component(clarifai_tags, all_components)
  if len(some_comp) > 0:
    return some_comp
  vector = tags_to_vector(clarifai_tags)
  probs = list(clf.predict_log_proba(vector)[0])
  lowest_score = min(probs)
  probs += [lowest_score-1]*(len(all_components) - len(probs))
  probs_with_tags = zip(probs, all_components)
  probs_with_tags.sort(reverse=True)
  components_in_order = map(lambda x: x[1], probs_with_tags)
  # Remove kumquat, plantain, pluot
  components_in_order = filter(lambda x: x.id not in [24, 45, 49, 13], components_in_order)
  return components_in_order

def find_top_component(clarifai_tags, all_components):
  top_tag = clarifai_tags[0][0]
  for component in all_components:
    if component.name.lower() == top_tag.lower():
      return [component]
  # second best tag?
  if clarifai_tags[1][1] > 0.98:
    top_tag = clarifai_tags[1][0]
    for component in all_components:
      if component.name.lower() == top_tag.lower():
        return [component]
  return []

def request_to_img_object(request):
  image_data = request.files.get('docfile', None)
  # form_data = ''.join(request.form.keys())
  # print image_data, file_data
  # print dir(request)
  if image_data != None:
    # It's from a phone!
    stream_data = image_data.stream.read()
    img_data = cStringIO.StringIO(stream_data)
    img = Image.open(img_data)
    return img
  # if form_data not in ['', None]:
  #   # It's from Postman!
  #   # stream_data = file_data.stream.read()
  #   # img_data = cStringIO.StringIO(stream_data)
  #   file = cStringIO.StringIO(form_data)
  #   img = Image.open(file)
  #   return img
  

def request_to_video_object(request):
  raw_video_data = request.files.get('docfile', None)
  if raw_video_data != None:
    # It's from a phone!
    stream_data = raw_video_data.stream.read()
    binary_data = cStringIO.StringIO(stream_data)
    #img = Image.open(img_data)
    return binary_data
  

def guess_components(img):
  global food_model
  global general_model
  if img == None:
    return [Component.query.first()], []
  img_byte_arr = io.BytesIO()
  img.save(img_byte_arr, format='JPEG')
  img_bytes = img_byte_arr.getvalue()
  
  guesses = get_clarifai_guesses_from_bytes(img_bytes)
  food_clarifai_tags = guesses['food']
  general_clarifai_tags = guesses['general']
  # food_clarifai_tags = get_clarifai_guess_from_bytes(img_bytes, food_model)
  # general_clarifai_tags = get_clarifai_guess_from_bytes(img_bytes, general_model)
  image_type = infer_image_type(general_clarifai_tags)
  tags_to_return = food_clarifai_tags if image_type == 'food' else general_clarifai_tags
  components_guesses = clarifai_tags_to_components_list(food_clarifai_tags)
  return image_type, components_guesses, tags_to_return

def infer_image_type(general_clarifai_tags):
  human_tags = ['man', 'woman', 'adult', 'face', 'nose', 'ear', 'glasses', 'pretty', 'smile', 'sexy', 'girl', 'boy', 'child', 'baby', 'human', 'people', 'men', 'women', 'children', 'faces']
  fruit_tags = ['fruit', 'food', 'apple', 'apricot', 'avocado', 'banana', 'blackberry', 'blackcurrant', 'blood orange', 'blueberry', 'cantaloupe', 'cherimoya', 'cherry', 'clementine', 'coconut', 'cranberry', 'cucumber', 'currant', 'date', 'dragonfruit', 'durian', 'fig', 'grape', 'grapefruit', 'guava', 'honeydew', 'jackfruit', 'kiwi', 'kumquat', 'lemon', 'lime', 'lychee', 'mandarine', 'mango', 'mangosteen', 'melon', 'nectarine', 'olive', 'orange', 'papaya', 'passionfruit', 'peach', 'pear', 'persimmon', 'pineapple', 'plantain', 'plum', 'pluot', 'pomegranate', 'prune', 'raisin', 'rambutan', 'raspberry', 'star fruit', 'strawberry', 'tamarind', 'tangerine', 'watermelon']
  has_human_tag, has_fruit_tag = False, False
  for classification, prob in general_clarifai_tags:
    if prob > 0.95:
      if classification in human_tags:
        has_human_tag = True
    if prob > 0.90:
      if classification in fruit_tags:
        has_fruit_tag = True
  if has_fruit_tag:
    return 'food'
  if has_human_tag:
    return 'person'
  return 'not food'

def get_clarifai_guesses_from_bytes(img_bytes):
  base64_bytes = base64.b64encode(img_bytes).decode('UTF-8')
  data = {
    'inputs': [
      {
        'data': {
          'image': {
            'base64': base64_bytes
          }
        }
      }
    ]
  }
  headers = {
    'Content-Type': 'application/json',
    'X-Clarifai-Client': 'python:2.0.14',
    'Authorization': 'Bearer %s' % CLARIFAI_AUTH_TOKEN
  }
  food_url = 'https://api.clarifai.com/v2/models/bd367be194cf45149e75f01d59f77ba7/outputs'
  general_url = 'https://api.clarifai.com/v2/models/aaa03c23b3724a16a56b629203edc62c/outputs'
  request_params = [
    { # Food API
      'url' : food_url,
      'method' : 'POST',
      'data' : data,
      'headers' : headers
    },
    { # General API
      'url' : general_url,
      'method' : 'POST',
      'data' : data,
      'headers' : headers
    }
  ]
  pr = ParallelRequester(request_params, 2)
  pr.run()
  results_dict = pr.results
  food_results = results_dict[food_url].json()
  general_results = results_dict[general_url].json()
  out = {}
  parsed_food_results = []
  try:
    results = food_results['outputs'][0]['data']['concepts']
    for result in results:
      prob = result['value']
      classification = result['name']
      parsed_food_results.append((classification, prob))
  except Exception as e:
    pass
  parsed_general_results = []
  try:
    results = general_results['outputs'][0]['data']['concepts']
    for result in results:
      prob = result['value']
      classification = result['name']
      parsed_general_results.append((classification, prob))
  except Exception as e:
    pass
  
  out['food'] = parsed_food_results
  out['general'] = parsed_general_results
  return out