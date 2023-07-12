import multiprocessing
import random
from functools import partial

NCPUS = multiprocessing.cpu_count()
print(f"We have {NCPUS} cores to work on!")


def parallel_dynamic_programming(dp_function, threads=max(1, NCPUS-2)):
    manager = multiprocessing.Manager()
    memoize_dict = manager.dict()
    lock = manager.Lock()
    pool = multiprocessing.Pool()

    func = partial(dp_function, lock, memoize_dict)
    pool.map(func, range(threads))
    pool.close()
    pool.join()
    return memoize_dict



def dp_function(lock, memoize_dict, _):
    def set_memoize(key, value):
        lock.acquire()
        memoize_dict[key]=value
        lock.release()

    for i in range(10):
        key = random.randint(0,100000)
        value = random.randint(0,100)
        set_memoize(key, value)

if __name__ == "__main__":
    a = parallel_dynamic_programming(dp_function)
    print(a)
    print(len(a))