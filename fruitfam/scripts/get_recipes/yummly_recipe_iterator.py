

class RecipeIterator(object):
  """Gives a bunch of recipes"""
  def __init__(self, searchterm):
    self.searchterm = searchterm
  
  def __iter__(self):
    return self
  
  def next(self):
    pass