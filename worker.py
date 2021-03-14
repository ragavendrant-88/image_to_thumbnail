from api import app_celery

celery = app_celery.createWorker()
