from fruitfam.scripts.test_svm.svm_test import SVMTest

class TopTwo(SVMTest):
  """Uses top two clarifai tags to possibly bypass SVM"""
  def __init__(self, image_to_components, svm_location, clarifai_tags_location):
    super(TopTwo, self).__init__(image_to_components, svm_location, clarifai_tags_location)
  
  def clarifai_tags_to_components_list(self, all_clarifai_tags, clf):
    all_components = self.all_components
    all_components.sort(key=lambda x: x.id)
    
    out = {}
    for image_url in all_clarifai_tags:
      clarifai_tags = all_clarifai_tags[image_url]
      if clarifai_tags == None:
        return None
      bypass_guess = self.find_top_component(clarifai_tags)
      if len(bypass_guess) > 0:
        out[image_url] = bypass_guess[0].id
        continue
      vector = self.tags_to_vector(clarifai_tags)
      probs = list(clf.predict_log_proba([vector])[0])
      lowest_score = min(probs)
      probs += [lowest_score-1]*(len(all_components) - len(probs))
      probs_with_tags = zip(probs, all_components)
      probs_with_tags.sort(reverse=True)
      components_in_order = map(lambda x: x[1], probs_with_tags)
      out[image_url] = components_in_order[0].id
    return out
  
  def find_top_component(self, clarifai_tags):
    all_components = self.all_components
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