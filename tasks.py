import time
from random import randint

from celery.utils.log import get_task_logger

from mycelery import app

logger = get_task_logger(__name__)


@app.task()
def compute_complex_task(x, y):
    duration = randint(3, 10)
    logger.info('Adds {0} + {1}. Duration {2}'.format(x, y, duration))
    time.sleep(duration)
    result = x + y

    return result
