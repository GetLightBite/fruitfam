# FruitFam

FruitFam is a game to help you get fitter by eating more. This is the server, which runs on python2.7. It's written using Flask. There are two parts - the main server, and a celery queue - which is used for offloading batch tasks like notifications.

## Running

Run the server locally with `python run.py`

## Deploying

Deploy the server with celery in devel with `python deploy.py`
Deploy the server with celery in prod with `python deploy.py --prod`

## Celery

Run celery locally in devel with `python launch_celery.py --devel`
Run celery locally in prod with `python launch_celery.py --prod`