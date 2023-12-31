import multiprocessing
from functools import partial

NCPUS = multiprocessing.cpu_count()
RESULT_KEY_IN_MEMODICT = "result_of_the_dp_function"


def parallel_dynamic_programming(
    dp_function, dp_fn_args=None, dp_fn_kwargs=None, threads=None
):
    threads = threads or max(1, NCPUS - 2)
    manager = multiprocessing.Manager()
    memoize_dict = manager.dict()
    lock = manager.Lock()
    run_done_event = manager.Event()

    dp_fn_args = dp_fn_args or []
    dp_fn_kwargs = dp_fn_kwargs or {}
    dp_function = partial(dp_function, *dp_fn_args, **dp_fn_kwargs)
    func = partial(dp_function_wrapped, dp_function, lock, memoize_dict, run_done_event)

    pool = multiprocessing.Pool()
    pool.map_async(func, range(threads))
    run_done_event.wait()
    pool.terminate()
    pool.join()

    return memoize_dict[RESULT_KEY_IN_MEMODICT]


def dp_function_wrapped(dp_fn, lock, memoize_dict, run_done_event, _):
    def set_memoize(key, value):
        lock.acquire()
        memoize_dict[key] = value
        lock.release()

    def get_memoize(key):
        value = memoize_dict.get(key)
        return value

    result = dp_fn(set_memoize=set_memoize, get_memoize=get_memoize)
    set_memoize(RESULT_KEY_IN_MEMODICT, result)
    run_done_event.set()
    return result
