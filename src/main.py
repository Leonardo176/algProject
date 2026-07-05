#!/usr/bin/env python3

from tests.test import TreeType, test_insertion

def main():
    test_insertion(TreeType.AVL)
    test_insertion(TreeType.BST)
    test_insertion(TreeType.RBT)

if __name__ == "__main__":
    main()