from random import Random
from sys import stderr

from trees.rbt import RBTree

if __name__ == "__main__":
    stderr.write("[ERROR] This file is a module\n")
    exit(-1)


def test_insert_height():
    rng = Random()
    # the random interval to generate numbers to be inserted
    rand_range = (0, 100000)
    to_insert = 10000
    rbt = RBTree()
    arr = []

    for _ in range(to_insert):
        n = rng.randint(rand_range[0], rand_range[1])
        # we don't want to insert the same items into the array or the bst
        if n not in arr:
            arr.append(n)
            rbt.insert_key(n)

    arr.sort()

    print(rbt.height())

    # the tree is a bst if and only if its inorder visit is sorted
    assert arr == rbt.inorder()


def test_rbt_insert_and_remove():
    rng = Random()
    # the random interval to generate numbers to be inserted
    rand_range = (0, 100000)
    to_insert = 10000
    rbt = RBTree()
    arr = []
    for _ in range(to_insert):
        if len(arr) == 0 or rng.randint(0, 1) == 0:
            n = rng.randint(rand_range[0], rand_range[1])
            # we don't want to insert the same items into the array or the bst
            if n not in arr:
                arr.append(n)
                rbt.insert_key(n)
        else:
            n = rng.randint(0, len(arr) - 1)
            rbt.remove(rbt.find(arr[n]))
            arr.remove(arr[n])

    arr.sort()

    # the tree is a bst if and only if its inorder visit is sorted
    assert arr == rbt.inorder()
