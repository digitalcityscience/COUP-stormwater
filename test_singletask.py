import time

from tasks import minus

if __name__ == '__main__':

    result = minus.delay(4, 4)
    result_available = False
    result.get()
    # while not result_available:
    #     time.sleep(1)
    #     result_available = result.ready()
    #     if result_available:
    #         print("Result is ready. The result is {}.".format(result.get()))
    #     else:
    #         print("Result is not ready. Lets keep waiting.")
