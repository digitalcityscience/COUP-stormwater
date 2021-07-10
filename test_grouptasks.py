import time

from celery import group

from models import ComplexTask
from tasks import compute_complex_task

if __name__ == '__main__':

    # Generate TestData
    tasks = [ComplexTask(param_a=i, param_b=i) for i in range(20)]
    task_group = group([compute_complex_task.s(taskParam.param_a, taskParam.param_b) for taskParam in tasks])

    group_result = task_group.apply_async()

    # Wait for result via polling.
    results_ready = False
    while not results_ready:
        results_ready = group_result.ready()

        print("Results ready:", group_result.completed_count())
        for result in group_result.results:
            print(result.state)
            print(result.ready())
        time.sleep(1)

        if results_ready:
            print(group_result.get())
