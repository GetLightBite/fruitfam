import requests

def get_directions_from_url(url):
  url='http://recipe-api.appspot.com/?url=' + url
  r = requests.get(url)
  resp = r.json()
  try:
    directions = [x['instruction'] for x in resp['recipe']['page_recipe_instructions']]
    if len(directions) == 0:
      return None
    return directions
  except Exception as e:
    # print url
    # print 'passing due to %s' % e
    return None