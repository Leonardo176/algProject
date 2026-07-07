#!/usr/bin/env python3

from tests.setup_test import TreeType, calc_lista_val_n
from tests.test_insertions import insertion_plot
from tests.test_rotations import rotations_plot
from tests.test_heights import heights_plot

import argparse

def main():
    #insertion_plot(TreeType.AVL, TreeType.BST, TreeType.RBT)
    #rotations_plot(TreeType.AVL, TreeType.RBT)
    #heights_plot(TreeType.AVL, TreeType.BST, TreeType.RBT)
    print(calc_lista_val_n())

    trees = [TreeType(t) for t in args.trees]

    if "insertion" in args.plot:
        insertion_plot(*trees)
    if "rotations" in args.plot:
        rotations_plot(*trees)
    if "heights" in args.plot:
        heights_plot(*trees)

if __name__ == "__main__":
    main()
