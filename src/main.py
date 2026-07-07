#!/usr/bin/env python3

from tests.setup_test import TreeType
from tests.test_insertions import insertion_plot
from tests.test_rotations import rotations_plot
from tests.test_heights import heights_plot

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", nargs="+", choices=["insertion", "rotations", "heights"], default=["insertion", "rotations", "heights"], help="What graph(s) to plot")
    parser.add_argument("--trees", nargs="+", choices=["AVL", "BST", "RBT"], default=["AVL", "BST", "RBT"], help="What tree(s) to plot")
    args = parser.parse_args()

    trees = [TreeType(t) for t in args.trees]

    if "insertion" in args.plot:
        insertion_plot(*trees)
    if "rotations" in args.plot:
        rotations_plot(*trees)
    if "heights" in args.plot:
        heights_plot(*trees)

if __name__ == "__main__":
    main()
