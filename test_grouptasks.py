import time

from celery import group

from tasks import process_something

task_group = group([
    process_something.s(4, 4),
    process_something.s(8, 8),
    process_something.s(16, 16),
    process_something.s(32, 32),
])

group_result = task_group.apply_async()

results_ready = False
while not results_ready:
    results_ready = group_result.ready()

    print("Results ready:", group_result.completed_count())
    for result in group_result.results:
        print(result.ready())
    time.sleep(1)

    if results_ready:
        print(group_result.get())
