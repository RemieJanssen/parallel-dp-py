import random
import time

from phylox.generators.trees.beta_splitting_tree import simulate_beta_splitting
from phylox.generators.trees.add_edges import AddEdgeMethod, network_from_tree

from parallel import parallel_dynamic_programming


def do_stuff(set_memoize=None, get_memoize=None):
    for i in range(10):
        time.sleep(1)
        key = random.randint(0, 100)
        value = random.randint(0, 100)
        set_memoize(key, value)
        for j in range(10):
            key = random.randint(0, 100)
            get_memoize(key)


def count_leaves(tree, set_memoize=None, get_memoize=None):
    def recursion(node):
        if (result := get_memoize(node)) is not None:
            return result
        time.sleep(0.01)
        if tree.is_leaf(node):
            set_memoize(node, 1)
            return 1
        count_leaves_below = 0
        children = list(tree.successors(node))
        random.shuffle(children)
        for child in children:
            count_leaves_below += recursion(child)
        set_memoize(node, count_leaves_below)
        return count_leaves_below

    root = list(tree.roots)[0]
    return recursion(root)


if __name__ == "__main__":
    leaves = 100
    reticulations = 100
    tree = simulate_beta_splitting(n=leaves, beta=1.0)
    network = network_from_tree(tree, reticulations, AddEdgeMethod.UNIFORM)
    for threads in [1,2,5,10]:
        start = time.time()
        # a = parallel_dynamic_programming(do_stuff, threads=threads)
        a = parallel_dynamic_programming(count_leaves, dp_fn_args=[network], threads=threads)
        total_time = time.time() - start
        print(a)
        print("threads", threads)
        print("time", total_time)
