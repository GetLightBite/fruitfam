from save_recipes import *

fruits = ['Apple', 'Apricot', 'Avocado', 'Banana', 'Blackberry', 'Blackcurrant', 'Blood orange', 'Blueberry', 'Cantaloupe', 'Cherimoya', 'Cherry', 'Clementine', 'Coconut', 'Cranberry', 'Cucumber', 'Currant', 'Date', 'Dragonfruit', 'Durian', 'Fig', 'Grape', 'Grapefruit', 'Guava', 'Honeydew', 'Jackfruit', 'Kiwi', 'Kumquat', 'Lemon', 'Lime', 'Lychee', 'Mandarine', 'Mango', 'Mangosteen', 'Melon', 'Nectarine', 'Olive', 'Orange', 'Papaya', 'Passionfruit', 'Peach', 'Pear', 'Persimmon', 'Pineapple', 'Plantain', 'Plum', 'Pluot', 'Pomegranate', 'Prune', 'Raisin', 'Rambutan', 'Raspberry', 'Star fruit', 'Strawberry', 'Tamarind', 'Tangerine', 'Watermelon']

for fruit in fruits:
  query1 = fruit + ' smoothie'
  query2 = fruit + ' salad'
  query3 = fruit + ' bowl'
  
  query_1_num_results = 30
  query_2_num_results = 50
  query_3_num_results = 20
  
  query1_cur_num_results = get_num_results_saved(query1)
  query2_cur_num_results = get_num_results_saved(query2)
  query3_cur_num_results = get_num_results_saved(query3)
  
  print 'get %d results for %s' % (query_1_num_results - query1_cur_num_results, query1)
  print 'get %d results for %s' % (query_2_num_results - query2_cur_num_results, query2)
  print 'get %d results for %s' % (query_3_num_results - query3_cur_num_results, query3)
  
  save_recipes(fruit, query1, query_1_num_results - query1_cur_num_results)
  save_recipes(fruit, query2, query_2_num_results - query2_cur_num_results)
  save_recipes(fruit, query3, query_3_num_results - query3_cur_num_results)