#!/usr/bin/env python3

from tests.bst import test_insert, test_insert_and_remove, test_rotate
from tests.rbt import test_insert_height, test_rbt_insert_and_remove


def main():
    print("BST tests:")

    test_insert()
    test_insert_and_remove()
    test_rotate()

    print("RBT tests:")

    test_insert_height()
    test_rbt_insert_and_remove()


if __name__ == "__main__":
    main()
