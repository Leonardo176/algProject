#!/usr/bin/env python3

from tests.test import TreeType, insertion_plot

def main():
    insertion_plot(TreeType.AVL, TreeType.BST, TreeType.RBT)

if __name__ == "__main__":
    main()