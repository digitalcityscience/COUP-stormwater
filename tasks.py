import time
from random import randint

from celery import signals
from celery.utils.log import get_task_logger

from cache import Cache
from mycelery import app

logger = get_task_logger(__name__)
cache = Cache()


@app.task()
def compute_complex_task(x, y) -> dict:
    # Check cache. If cached, return result from cache.
    key = str(hash((x, y)))
    result = cache.retrieve(key=key)
    if not result == {}:
        return result

    # Start computing
    duration = randint(3, 10)
    logger.info('Adds {0} + {1}. Duration {2}'.format(x, y, duration))
    time.sleep(duration)
    result = x + y

    return {"sum": result}


@signals.task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    state = kwargs.get('state')
    args = kwargs.get('args')
    result = kwargs.get('retval')

    # Cache only succeeded tasks
    if state == "SUCCESS":
        key = str(hash(tuple(args)))
        cache.save(key=key, value=result)
