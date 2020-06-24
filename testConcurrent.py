from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from threading import current_thread # SOLUTION
import itertools

def test(a, b):
    result = []
    for i in b:
        result.append(a+i)
    return result

def main(a, b):
    arr = []
    with ProcessPoolExecutor(max_workers=10) as executor:
        for r in [executor.submit(test, i, b)
                           for i in a]:
            print(r.result())

        # for future in as_completed(future_to_stuff):
        #     arr.append(future.result())
    print(arr)

if __name__ == '__main__':
    a = [1, 1,1,2]
    b = [1,1,1,1]
    main(a, b)
