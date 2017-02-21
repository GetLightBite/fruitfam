import json

list_of_incorrect_images_file = open('exclude_images.json', 'r')
list_of_incorrect_images = json.loads(list_of_incorrect_images_file.read())
list_of_incorrect_images_file.close()

current_test_images_file = open('test_images.json', 'r')
current_test_images = json.loads(current_test_images_file.read())
current_test_images_file.close()

for fruit in current_test_images:
  test_images = current_test_images[fruit]
  new_images = set(test_images) - set(list_of_incorrect_images)
  images_removed = set(test_images) - new_images
  print images_removed
  current_test_images[fruit] = list(new_images)

current_test_images_file = open('filtered_test_images.json', 'w')
current_test_images_file.write(json.dumps(current_test_images))
current_test_images_file.close()