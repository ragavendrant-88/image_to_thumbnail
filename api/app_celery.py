from flask import Flask
from api import config, tasks

def createApp():
    return entryPoint(mode='app')


def createWorker():
    return entryPoint(mode='worker')


def entryPoint(mode='app'):
    app = Flask(__name__)
    app.config['CELERY_BROKER_URL'] = config.CELERY['BROKER_URL']
    app.config['CELERY_RESULT_BACKEND'] = config.CELERY['RESULT_BACKEND']

    configureCelery(app, tasks.celery)

    if mode == 'app':
        return app
    elif mode == 'worker':
        return tasks.celery


def configureCelery(app, celery):

    # Set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # Subclass task base for app context
    task_base = celery.Task

    class AppContextTask(task_base):

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = AppContextTask

    # Run finalize to process decorated tasks
    celery.finalize()