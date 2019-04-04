# Run with:
#   `pipenv run celery -A app.tasks worker --loglevel=INFO`
#
#  from app.tasks import add_together
#  result = add_together.delay(1, 2)
#  result.wait()

from celery import Celery
from wsgi import app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task()
def very_slow_add(a, b):
    import time
    time.sleep(3)
    return a + b
