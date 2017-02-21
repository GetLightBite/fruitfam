To collect images from the kalekam project, copy the code in `collect_burrito_image.py` and paste into a kalekam repl in the burrito repo. A json file will be created with all the image urls in it.

To remove a list of incorrect image urls from this list, run `python filter_images.py`. The list of images to filter out are in `exclude_images.json`.

To form a mapping from image to current fruitfam components, navigate to the top level of the repo and run `python fruitfam/scripts/test_svm/filtered_image_to_fruitfam_component.py`

To test a trained SVM on a set of test images run `python test_svm.py`