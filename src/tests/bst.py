from random import Random
from sys import stderr

if __name__ == "__main__":
    stderr.write("[ERROR] This file is a module\n")
    exit(-1)


from trees.bst import BST


def test_insert():
    rng = Random()
    # the random interval to generate numbers to be inserted
    rand_range = (0, 100000)
    to_insert = 10000
    bst = BST()
    arr = []

    for _ in range(to_insert):
        n = rng.randint(rand_range[0], rand_range[1])
        # we don't want to insert the same items into the array or the bst
        if n not in arr:
            arr.append(n)
            bst.insert_key(n)

    arr.sort()

    print(bst.height())

    # the tree is a bst if and only if its inorder visit is sorted
    assert arr == bst.inorder()


def test_insert_and_remove():
    rng = Random()
    # the random interval to generate numbers to be inserted
    rand_range = (0, 10000)
    to_insert = 1000
    bst = BST()
    arr = []
    for _ in range(to_insert):
        if len(arr) == 0 or rng.randint(0, 1) == 0:
            n = rng.randint(rand_range[0], rand_range[1])
            # we don't want to insert the same items into the array or the bst
            if n not in arr:
                arr.append(n)
                bst.insert_key(n)
        else:
            n = rng.randint(0, len(arr) - 1)
            bst.remove(bst.find(arr[n]))
            arr.remove(arr[n])

    arr.sort()

    # the tree is a bst if and only if its inorder visit is sorted
    assert arr == bst.inorder()


def test_rotate():
    rng = Random()
    rand_range = (1, 10000)
    n = 1000
    bst = BST()
    arr = []

    for _ in range(n):
        n = rng.randint(rand_range[0], rand_range[1])
        # we don't want to insert the same items into the array or the bst
        if n not in arr:
            arr.append(n)
            bst.insert_key(n)

    # lets do some random rotations

    for _ in range(100):
        i = rng.randrange(len(arr))
        if rng.randrange(2) == 0:
            # print(f"Left: {arr[i]}")
            bst.rotate_left(bst.find(arr[i]))
        else:
            # print(f"Right: {arr[i]}")
            bst.rotate_right(bst.find(arr[i]))

    # print(arr)

    arr.sort()

    # print(arr)
    # print(bst.inorder())

    assert arr == bst.inorder()
