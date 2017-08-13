import json
import operator
import os
import sys

# add parent dir to PYTHONPATH
cur_path = os.path.abspath('../../..')
sys.path.insert(1, cur_path)
from fruitfam.models.component import Component

all_components = Component.query.all()
name_to_component = {x.name : x for x in all_components}

filtered_images_file = open('fruitfam/scripts/test_svm/filtered_test_images.json', 'r')
filtered_images = json.loads(filtered_images_file.read())
filtered_images_file.close()

all_images = list(set(reduce(operator.add, filtered_images.values())))


image_to_fruitfam_component_ids = {}
for image in all_images:
  # Get burrito fruit names
  burrito_fruit_names = []
  for fruit in filtered_images:
    if image in filtered_images[fruit]:
      burrito_fruit_names.append(fruit)
  
  # Get the fruitfam components:
  fruitfam_component_ids = []
  for fruit in burrito_fruit_names:
    fruitfam_component = name_to_component.get(fruit, None)
    if fruitfam_component != None:
      fruitfam_component_ids.append(fruitfam_component.id)
  if len(fruitfam_component_ids) > 0:
    image_to_fruitfam_component_ids[image] = fruitfam_component_ids

out_file = open('fruitfam/scripts/test_svm/image_to_fruitfam_component.json', 'w')
out_file.write(json.dumps(image_to_fruitfam_component_ids))
out_file.close()