web: gunicorn fruitfam:app --timeout 120 -k gevent --worker-connections 1000
celery: python launch_celery.py