#!/usr/bin/env python3

from tests.avl import test_avl_insert, test_avl_insert_and_remove
from tests.bst import test_bst_insert, test_bst_insert_and_remove, test_bst_rotate
from tests.rbt import test_rbt_insert_height, test_rbt_insert_and_remove

def main():
    print("AVL TESTS:\n")

    #test_avl_insert()
    test_avl_insert_and_remove()

    # print("\nBST tests:\n")

    # test_bst_insert()
    # test_bst_insert_and_remove()
    # test_bst_rotate()

    # print("\nRBT tests:\n")

    # test_rbt_insert_height()
    # test_rbt_insert_and_remove()

if __name__ == "__main__":
    main()