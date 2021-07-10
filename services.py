from celery import group
from celery.result import GroupResult

from models import ComplexTask
from tasks import compute_complex_task


def compute(complex_tasks: list) -> GroupResult:
    # Validate input
    for complexTask in complex_tasks:
        if type(complexTask) != ComplexTask:
            raise ValueError('Expected type ComplexTask but got %s' % type(complexTask))

    task_group = group([compute_complex_task.s(ct.param_a, ct.param_b) for ct in complex_tasks])
    group_result = task_group()
    group_result.save()

    return group_result
