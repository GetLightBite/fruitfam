# This file is for running all SVM tests
import json
# add parent dir to PYTHONPATH
import os
import sys
cur_path = os.path.abspath('../../..')
sys.path.insert(1, cur_path)

from fruitfam.scripts.test_svm.svm_test import SVMTest
from fruitfam.scripts.test_svm.top_two_plus_svm import TopTwo

test_set = {
  'https://s3.amazonaws.com/fruitfam/FRbdDcqkK8xEmIVw3VWFGZkuHFsq0WGK2R8xxClOBeZyHmpfjz' : [4],
  'https://s3.amazonaws.com/fruitfam/kwCEy3NkWk2KDi7VGk2cN40UeSi5Jj9K60QoOfHXYHeztUQ3oK' : [1]
}
# Load up the input images
test_set_file = open('fruitfam/scripts/test_svm/image_to_fruitfam_component.json', 'r')
test_set = json.loads(test_set_file.read())
test_set_file.close()

print '\n\n'
####################
# Test  Normal SVM #
####################
svm_location = '/users/avadrevu/workspace/fruitfam/fruitfam/bin/svm.pkl'
clarifai_tags = '/users/avadrevu/workspace/fruitfam/fruitfam/bin/clarifai_tags.json'
test1 = SVMTest(test_set, svm_location, clarifai_tags)
o = test1.run()
print 'Normal SVM'
test1.print_results()
print '\n\n'


######################
# Test  Filtered SVM #
######################
svm_location = '/users/avadrevu/workspace/fruitfam/fruitfam/bin/filtered_svm/svm_filtered.pkl'
clarifai_tags = '/users/avadrevu/workspace/fruitfam/fruitfam/bin/filtered_svm/clarifai_tags_filtered.json'
test2 = SVMTest(test_set, svm_location, clarifai_tags)
o = test2.run()
print 'Filtered SVM'
test2.print_results()
print '\n\n'

#####################################
# Use top two guesses to bypass SVM #
#####################################
svm_location = '/users/avadrevu/workspace/fruitfam/fruitfam/bin/filtered_svm/svm_filtered.pkl'
clarifai_tags = '/users/avadrevu/workspace/fruitfam/fruitfam/bin/filtered_svm/clarifai_tags_filtered.json'
test3 = TopTwo(test_set, svm_location, clarifai_tags)
o = test3.run()
print 'Top two guesses bypass SVM'
test3.print_results()
print '\n\n'