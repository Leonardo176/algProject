#!/usr/bin/env python3

from tests.setup_test import TreeType
from tests.test_insertions import insertion_plot
from tests.test_rotations import rotations_plot


def main():
    #insertion_plot(TreeType.AVL, TreeType.BST, TreeType.RBT)
    rotations_plot(TreeType.AVL, TreeType.RBT)


if __name__ == "__main__":
    main()
