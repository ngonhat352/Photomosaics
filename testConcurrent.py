from concurrent import futures
import threading
import time


def task(n):
    print('{}: sleeping {}'.format(
        threading.current_thread().name,
        n)
    )
    time.sleep(n / 10)
    print('{}: done with {}'.format(
        threading.current_thread().name,
        n)
    )
    return n / 10


ex = futures.ThreadPoolExecutor(max_workers=2)
print('main: starting')
results = ex.map(task, range(5, 0, -1))
print('main: unprocessed results {}'.format(results))
print('main: waiting for real results')
real_results = list(results)
print('main: results: {}'.format(real_results))
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from threading import current_thread # SOLUTION
# import itertools
#
# def test(a, b):
#     result = []
#     for i in b:
#         result.append(a+i)
#     return result
#
# def main(a, b):
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         future_to_stuff = [executor.submit(test, i, b)
#                            for i in a]
#
#         for future in as_completed(future_to_stuff):
#             print(future.result())
#
#
# if __name__ == '__main__':
#     a = [1, 1,1,2]
#     b = [1,1,1,1]
#     main(a, b)
