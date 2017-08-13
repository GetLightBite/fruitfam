# get all fruit images in burrito
# runs in a burrito repl

fruit_components = Component.query.filter(Component.is_fruit==True).all()
all_food_items = FoodItem.query.all()

# Get all the fruit images
component_to_food_items = {}
for fruit_component in fruit_components:
  fruit_component_id = fruit_component.id
  matching_food_items = []
  for food_item in all_food_items:
    tags = food_item.get_components()
    if tags != []:
      for categorization_attempt in tags:
        if type(categorization_attempt) == list:
          if fruit_component_id in categorization_attempt:
            matching_food_items.append(food_item)
            break
  print matching_food_items
  print len(matching_food_items)
  component_to_food_items[fruit_component] = matching_food_items

# Get images into json format
out_json = {}
for component in component_to_food_items:
  food_items_list = component_to_food_items[component]
  images = []
  for food_item in food_items_list:
    image = food_item.img_url_recognition
    if image == None:
      image = food_item.cdn_img_url_large()
    if image == None:
      image = food_item.cdn_img_url_fullscreen()
    images.append(image)
  images = filter(None, images)
  print component, len(images)
  out_json[component.name] = images

# Write to disk
k = open('test_images.json', 'w')
k.write(json.dumps(out_json))
k.close()