from google_images import *
import json

fruits_list = ['Apple', 'Apricot', 'Avocado', 'Banana', 'Blackberry', 'Blackcurrant', 'Blueberry', 'Currant', 'Cherry', 'Cherimoya', 'Coconut', 'Cranberry', 'Cucumber', 'Date', 'Dragonfruit', 'Durian', 'Fig', 'Grape', 'Raisin', 'Grapefruit', 'Guava', 'Jackfruit', 'Kiwi', 'Kumquat', 'Lemon', 'Lime', 'Lychee', 'Mango', 'Melon', 'Cantaloupe', 'Honeydew', 'Watermelon', 'Nectarine', 'Olive', 'Orange', 'Blood orange', 'Clementine', 'Mandarine', 'Tangerine', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Plantain', 'Plum', 'Prune', 'Pineapple', 'Pluot', 'Pomegranate', 'Mangosteen', 'Raspberry', 'Rambutan', 'Star fruit', 'Strawberry', 'Tamarind'
]

def search_term(term):
  if term == 'Apple':
    return 'Apple fruit'
  elif term == 'Blackberry':
    return 'Blackberry fruit'
  return term


if __name__ == '__main__':
  doc = open('search_results.json', 'r')
  cur_results = doc.read()
  doc.close()
  search_results = json.loads(cur_results)
  for fruit in fruits_list:
    list_of_results = search_results.get(fruit, [])
    if len(list_of_results) < 70:
      term = search_term(fruit)
      results = image_results_iterator(term)
      for result in results:
        print 'adding to %s %s' % (fruit, result)
        # Add this to search results and save the json
        list_of_results = search_results.get(fruit, [])
        list_of_results.append(result)
        list_of_results = list(set(list_of_results))
        search_results[fruit] = list_of_results
        # save
        doc = open('search_results.json', 'w')
        doc.write(json.dumps(search_results))
        doc.close()