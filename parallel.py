import multiprocessing
import random
import time

from functools import partial


NCPUS = multiprocessing.cpu_count()
print(f"We have {NCPUS} cores to work on!")


def parallel_dynamic_programming(dp_function, threads=None):
    threads = threads or max(1, NCPUS-2)
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

    def get_memoize(key):
        return memoize_dict.get(key)

    for i in range(100):
        key = random.randint(0,100)
        value = random.randint(0,100)
        set_memoize(key, value)
        for i in range(100):
            key = random.randint(0,100)
            get_memoize(key)


if __name__ == "__main__":
    threads = 8
    start = time.time()
    a = parallel_dynamic_programming(dp_function, threads=threads)
    total_time = time.time() - start
    print(a)
    print(len(a))
    print("threads", threads)
    print("time", total_time)