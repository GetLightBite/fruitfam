from sklearn import metrics

class Test(object):
  """class for testing any SVM or recognition system"""
  def __init__(self, image_to_components):
    self.images = image_to_components.keys()
    self.image_to_components = image_to_components
    self.image_to_results = {}
  
  def run(self):
    """
    Populates image_to_results
    """
    pass
  
  def print_results(self):
    expected_results = []
    predicted_results = []
    for image in self.image_to_components:
      correct_component_ids = self.image_to_components[image]
      if len(correct_component_ids) > 0:
        guessed_component_id = self.image_to_results[image]
        if guessed_component_id in correct_component_ids:
          predicted_results.append(guessed_component_id)
          expected_results.append(guessed_component_id)
        else:
          predicted_results.append(guessed_component_id)
          expected_results.append(correct_component_ids[0])
    classification_report = metrics.classification_report(expected_results, predicted_results)
    print classification_report