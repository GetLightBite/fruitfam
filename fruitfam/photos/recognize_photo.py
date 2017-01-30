from clarifai.rest import ClarifaiApp
import cString
import Image
import io

os.environ["CLARIFAI_APP_ID"] = "dzsFD42XCHlRhIzIs6qz25TUGNFfKQYT3mnib6C7"
os.environ["CLARIFAI_APP_SECRET"] = "XRG4Fo_p9zyFDNxmjg36EVEqQ3fqywkmyTvDLPLe"

########################################
# Set up reusable data in global scope #
########################################

clarifai_app, food_model = None, None
try:
  print 'starting clarifai app...'
  clarifai_app = ClarifaiApp()
  food_model = clarifai_app.models.get('food-items-v1.0')
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

clf = joblib.load('/users/avadrevu/workspace/fruitfam/fruitfam/bin/svm.pkl')

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

def guess_components(image_data):
  stream_data = image_data.stream.read()
  img_data = cStringIO.StringIO(stream_data)
  img = Image.open(img_data)
  img_byte_arr = io.BytesIO()
  img.save(img_byte_arr, format='JPEG')
  img_bytes = img_byte_arr.getvalue()
  
  clarifai_tags = get_clarifai_guess_from_bytes(img_bytes)
  components_guesses = clarifai_tags_to_components_list(clarifai_tags)
  return components_guesses

def get_clarifai_guess_from_bytes(img_bytes):
  global food_model
  resp = food_model.predict_by_bytes(img_bytes)
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