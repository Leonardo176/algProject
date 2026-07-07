#!/usr/bin/env python3

from tests.setup_test import TreeType, calc_lista_val_n
from tests.test_insertions import insertion_plot
from tests.test_rotations import rotations_plot
from tests.test_heights import heights_plot


def main():
    #insertion_plot(TreeType.AVL, TreeType.BST, TreeType.RBT)
    #rotations_plot(TreeType.AVL, TreeType.RBT)
    #heights_plot(TreeType.AVL, TreeType.BST, TreeType.RBT)
    print(calc_lista_val_n())


if __name__ == "__main__":
    main()
