from celery.task.control import discard_all

# Clear the redis queue
print 'Clearing queue'
discard_all()

from fruitfam import celery