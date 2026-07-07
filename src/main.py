#!/usr/bin/env python3

from tests.setup_test import TreeType
from tests.test_insertions import insertion_plot
from tests.test_rotations import rotations_plot
from tests.test_heights import heights_plot

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", nargs="+", choices=["insertions", "rotations", "heights"], default=["insertions", "rotations", "heights"], help="What graph(s) to plot")
    
    parser.add_argument("--trees", nargs="+", choices=["AVL", "BST", "RBT"], default=["AVL", "BST", "RBT"], help="What tree(s) to plot")
    
    parser.add_argument("--n", type=int, default=1000000, help="Maximum number of nodes")
    
    args = parser.parse_args()
    
    if args.n < 1000:
        parser.error("n has to be greater than 1000 ")

    trees = [TreeType(t) for t in args.trees]

    if "insertions" in args.plot:
        insertion_plot(args.n, *trees)
    if "rotations" in args.plot:
        rotations_plot(args.n, *trees)
    if "heights" in args.plot:
        heights_plot(args.n, *trees)

if __name__ == "__main__":
    main()