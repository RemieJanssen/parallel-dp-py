import random
import time

from phylox.generators.trees.beta_splitting_tree import simulate_beta_splitting
from phylox.generators.trees.add_edges import AddEdgeMethod, network_from_tree

from parallel import parallel_dynamic_programming


def do_stuff(memoize_dict=None):
    for _ in range(1000):
        key = random.randint(0, 1000)
        if key in memoize_dict:
            continue
        time.sleep(.05)
        value = key
        memoize_dict[key] = value
    return [(x, y) for x,y in memoize_dict.items()]


def count_paths_to_leaves(tree, memoize_dict=None):
    def recursion(node):
        if (result := memoize_dict.get(node)) is not None:
            return result
        time.sleep(0.01)
        if tree.is_leaf(node):
            memoize_dict[node] = 1
            return 1
        count_leaves_below = 0
        children = list(tree.successors(node))
        random.shuffle(children)
        for child in children:
            count_leaves_below += recursion(child)
        memoize_dict[node] = count_leaves_below
        return count_leaves_below

    root = list(tree.roots)[0]
    return recursion(root)


if __name__ == "__main__":
    leaves = 200
    reticulations = 200
    tree = simulate_beta_splitting(n=leaves, beta=1.0)
    network = network_from_tree(tree, reticulations, AddEdgeMethod.UNIFORM)
    for threads in [1,2,5,10,15,20,None]:
        start = time.time()
        a = parallel_dynamic_programming(do_stuff, threads=threads)
        # a = parallel_dynamic_programming(count_paths_to_leaves, dp_fn_args=[network], threads=threads)
        total_time = time.time() - start
        print(a)
        print("threads", threads)
        print("time", total_time)
