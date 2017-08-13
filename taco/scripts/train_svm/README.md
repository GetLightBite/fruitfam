To download images from google, run `python upload_all_images.py`. This will store results in `search_results.json`.

To filter out bad images, run `python filter_images.py`. This creates the html file `images_to_filter.html`. Simply click on the images you don't like on the document. When you're done, open the javascript console in the browser and run `download()`. There will be a link at the bottom of the page to download all the bad image urls.

Then, to run all the results against Clarifai, run `python run_clarifai.py`. This stores clarifai results in `clarifai_results.json`

Then, to train an SVM, navigate to the top level of the repo and run `python fruitfam/scripts/train_svm/train_svm.py`