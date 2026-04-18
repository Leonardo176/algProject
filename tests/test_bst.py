from random import Random

from src.BST.BST import BinarySearchTree


def test_insert():
    rng = Random()
    # the random interval to generate numbers to be inserted
    rand_range = (0, 10000)
    to_insert = 1000
    bst = BinarySearchTree()
    arr = []

    for _ in range(to_insert):
        n = rng.randint(rand_range[0], rand_range[1])
        # we don't want to insert the same items into the array or the bst
        if n not in arr:
            arr.append(n)
            bst.insert(n)

    arr.sort()

    # the tree is a bst if and only if its inorder visit is sorted
    assert arr == bst.inorder()


def main():
    test_insert()


if __name__ == "__main__":
    main()
