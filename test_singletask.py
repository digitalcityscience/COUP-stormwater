import time

from tasks import compute_complex_task

if __name__ == '__main__':

    result = compute_complex_task.delay(4, 4)

    # Wait for result via polling.
    result_available = False
    while not result_available:
        time.sleep(1)
        result_available = result.ready()
        if result_available:
            print("Result is ready. The result is {}.".format(result.get()))
        else:
            print("Result is not ready. Lets keep waiting.")
