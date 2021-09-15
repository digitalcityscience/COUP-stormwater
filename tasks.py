import time
from random import randint

from celery import signals
from celery.utils.log import get_task_logger

from cache import Cache
from mycelery import app
from swimdock.main import perform_swmm_analysis

logger = get_task_logger(__name__)
cache = Cache()

sample = {
    "calculation_method": "normal",
    "hash": "yxz123",
    "model_updates": [
        {
            "outlet_id": "J_out19",
            "subcatchment_id": "Sub000"
        }
    ],
    "rain_event": {
        "duration": 120,
        "return_period": 10
    }
}


@app.task()
def compute_complex_task(complex_task: dict) -> dict:
    # Check cache. If cached, return result from cache.
    key = complex_task['hash']

    result = cache.retrieve(key=key)
    if not result == {}:
        return result

    # Start computing
    # duration = randint(3, 10)
    logger.info('Compute {0}'.format(key))
    # time.sleep(duration)
    result = perform_swmm_analysis(complex_task)

    return result


@signals.task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    state = kwargs.get('state')
    args = kwargs.get('args')
    result = kwargs.get('retval')

    # Cache only succeeded tasks
    if state == "SUCCESS":
        key = args[0]['hash']
        cache.save(key=key, value=result)
