To download images from google, run `python upload_all_images.py`. This will store results in `search_results.json`.

Then, to run all the results against Clarifai, run `python run_clarifai.py`. This stores clarifai results in `clarifai_results.json`

Then, to train an SVM, run `python train_svm.py`